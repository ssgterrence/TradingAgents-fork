"""Deterministic guard for the Portfolio Manager's multi-horizon views.

The horizon layer lets a run say "short-term Sell, long-term Hold", but a model
must not be trusted to keep the two apart on its own: it can cite a short-term
price drop as a long-term trend break, or call a not-yet-reached level "active".
This module applies the project's ground-truth principle to those claims:

- Price triggers are re-checked against the latest verified close.
- Trend triggers that name the 200SMA (or a 50/200 cross) are re-checked against
  the computed facts, and one that is contradicted is marked invalidated.
- A long-term Sell with no active long-term evidence is downgraded to Hold.

It is deterministic and testable; the LLM proposes, this module verifies.
"""

from __future__ import annotations

from tradingagents.agents.schemas import (
    HorizonStance,
    HorizonTrigger,
    PortfolioDecision,
    TriggerDirection,
    TriggerKind,
    TriggerStatus,
)
from tradingagents.dataflows import quality
from tradingagents.dataflows.vendors.yahoo.snapshot import build_horizon_facts

# Long-term Sell cannot rest on price alone; these are the kinds that count.
_LONG_TERM_EVIDENCE = {TriggerKind.TREND, TriggerKind.FUNDAMENTAL, TriggerKind.EVENT}

_LONG_TERM_TEXT = ("200", "long-term", "long term", "200-day", "200sma")


def build_horizon_evidence(ticker: str, trade_date: str) -> dict | None:
    """The deterministic facts for the horizon layer, or None when unavailable."""
    try:
        return build_horizon_facts(ticker, trade_date)
    except Exception as exc:  # noqa: BLE001 — evidence is optional; the run goes on
        quality.record("build_horizon_facts", "core_stock_apis", "failed",
                       ["yfinance"], failures=[("yfinance", type(exc).__name__)])
        return None


def render_horizon_evidence(facts: dict | None) -> str:
    """A compact prompt block the Portfolio Manager reads before writing triggers."""
    if not facts:
        return ""
    lines = [
        "## Deterministic horizon evidence (source of truth for price/trend triggers)",
        "",
    ]
    for key, label in (
        ("latest_date", "Latest close date"),
        ("close", "Latest close"),
        ("ema10", "10EMA"),
        ("sma50", "50SMA"),
        ("sma200", "200SMA"),
        ("sma200_slope_20d_pct", "200SMA 20-day slope (%)"),
        ("price_vs_sma200_pct", "Price vs 200SMA (%)"),
        ("rsi", "RSI"),
        ("atr", "ATR"),
        ("atr_pct", "ATR (% of close)"),
        ("vwma", "VWMA"),
    ):
        value = facts.get(key)
        lines.append(f"- {label}: {value if value is not None else 'N/A'}")
    lines += [
        "",
        "Use these numbers for price/trend triggers. Do not call a trigger active if this "
        "block shows its condition is not met, and do not treat a short-term price level as "
        "long-term trend evidence.",
    ]
    return "\n".join(lines) + "\n"


def _price_met(trigger: HorizonTrigger, close: float | None) -> bool | None:
    """Whether a price trigger's level is reached now, or None when it cannot be checked."""
    if trigger.kind != TriggerKind.PRICE or trigger.level is None or trigger.price_condition is None:
        return None
    if close is None:
        return None
    return close < trigger.level if trigger.price_condition == "below" else close > trigger.level


def _is_long_term_trend(trigger: HorizonTrigger) -> bool:
    text = f"{trigger.condition} {trigger.evidence or ''}".lower()
    return any(token in text for token in _LONG_TERM_TEXT)


def _trend_met(trigger: HorizonTrigger, facts: dict) -> bool | None:
    """Whether a trend trigger's claim is true now, or None when it cannot be checked."""
    text = f"{trigger.condition} {trigger.evidence or ''} {trigger.invalid_if or ''}".lower()
    close = facts.get("close")
    sma50 = facts.get("sma50")
    sma200 = facts.get("sma200")
    slope = facts.get("sma200_slope_20d_pct")
    is_cross = "death cross" in text or "golden cross" in text or ("50" in text and "200" in text)
    is_long = _is_long_term_trend(trigger)

    if trigger.direction == TriggerDirection.SELL:
        if is_long:
            if None in (close, sma200, slope):
                return None
            return close < sma200 and slope < 0
        if is_cross:
            if sma50 is None or sma200 is None:
                return None
            return sma50 < sma200
        return None
    # BUY
    if is_long:
        if None in (close, sma200, slope):
            return None
        return close > sma200 and slope > 0
    if is_cross:
        if sma50 is None or sma200 is None:
            return None
        return sma50 > sma200
    return None


def _validate_triggers(decision: PortfolioDecision, facts: dict) -> None:
    close = facts.get("close")
    for view in (decision.short_term, decision.mid_term, decision.long_term):
        for trigger in view.triggers:
            if trigger.kind == TriggerKind.PRICE:
                met = _price_met(trigger, close)
                if met is None:
                    continue
                if met and trigger.status != TriggerStatus.ACTIVE:
                    trigger.status = TriggerStatus.ACTIVE
                    trigger.status_reason = None
                elif not met and trigger.status == TriggerStatus.ACTIVE:
                    trigger.status = TriggerStatus.PENDING
                    trigger.status_reason = (
                        f"close {close} is not {'below' if trigger.price_condition == 'below' else 'above'} {trigger.level}"
                    )
            elif trigger.kind == TriggerKind.TREND:
                met = _trend_met(trigger, facts)
                if met is False:
                    trigger.status = TriggerStatus.INVALIDATED
                    trigger.status_reason = (
                        "the deterministic trend facts contradict this trigger "
                        "(see horizon evidence block)"
                    )
                elif met is True and trigger.status != TriggerStatus.ACTIVE:
                    trigger.status = TriggerStatus.ACTIVE
                    trigger.status_reason = None


def _long_term_supported(decision: PortfolioDecision, facts: dict) -> bool:
    """Whether an active long-term trigger justifies the long-term Sell.

    Price and sentiment triggers are not long-term evidence; a trend trigger must
    reference the 200SMA and be independently confirmed. Returns True when a real
    long-term trigger is active, or when one cannot be verified (so the view is
    not downgraded on a missing indicator).
    """
    for trigger in decision.long_term.triggers:
        if trigger.status != TriggerStatus.ACTIVE or trigger.direction != TriggerDirection.SELL:
            continue
        if trigger.kind in (TriggerKind.FUNDAMENTAL, TriggerKind.EVENT):
            return True
        if trigger.kind == TriggerKind.TREND:
            if not _is_long_term_trend(trigger):
                continue  # a 50SMA/price trigger is not long-term evidence
            met = _trend_met(trigger, facts)
            if met is True:
                return True
            if met is None:
                return True  # cannot verify, so do not downgrade on this
    return False


def apply_horizon_policy(decision: PortfolioDecision, facts: dict | None) -> list[str]:
    """Verify triggers and enforce the long-term rule; return the notes to surface.

    Mutates ``decision`` in place (trigger statuses, and possibly the long-term
    stance). The caller folds the returned notes into ``horizon_note``.
    """
    notes: list[str] = []
    if facts is None:
        notes.append(
            "Deterministic horizon evidence is unavailable this run; price/trend trigger "
            "statuses and the long-term guard were not independently verified."
        )
        return notes

    _validate_triggers(decision, facts)

    if decision.long_term.stance == HorizonStance.SELL and not _long_term_supported(decision, facts):
        decision.long_term.stance = HorizonStance.HOLD
        notes.append(
            "Long-term Sell downgraded to Hold: the cited evidence is short-term price "
            "action; no active long-term trend/fundamental/event trigger was found."
        )

    if decision.short_term.stance != decision.long_term.stance and not decision.horizon_note:
        decision.horizon_note = (
            "Horizons diverge: the short-term view is tactical and does not change the "
            "long-term view without its own long-term trigger."
        )
        notes.append("Added a horizon-divergence note (short-term differs from long-term).")

    return notes


def horizon_summary(decision: PortfolioDecision) -> dict:
    """The short/mid/long stances, for the report header."""
    return {
        "short": decision.short_term.stance.value,
        "mid": decision.mid_term.stance.value,
        "long": decision.long_term.stance.value,
    }
