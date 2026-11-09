"""The multi-horizon layer: schema defaults, deterministic policy, and rendering."""

from __future__ import annotations

import pandas as pd
import pytest

from tradingagents.agents.horizon import (
    apply_horizon_policy,
    horizon_summary,
    render_horizon_evidence,
)
from tradingagents.agents.schemas import (
    EvidenceSource,
    Horizon,
    HorizonStance,
    HorizonTrigger,
    HorizonView,
    PortfolioDecision,
    PortfolioRating,
    TriggerDirection,
    TriggerKind,
    TriggerStatus,
    render_pm_decision,
)
from tradingagents.dataflows.vendors.yahoo import snapshot

FACTS = {
    "latest_date": "2026-11-06",
    "close": 284.78,
    "ema10": 294.634,
    "sma50": 332.906,
    "sma200": 339.216,
    "sma200_slope_20d_pct": -0.52,
    "price_vs_sma200_pct": -16.0,
    "rsi": 29.92,
    "atr": 10.68,
    "atr_pct": 3.75,
    "vwma": 297.6,
}


def _trigger(
    horizon="long",
    direction=TriggerDirection.SELL,
    kind=TriggerKind.PRICE,
    status=TriggerStatus.ACTIVE,
    condition="close below 276.92",
    level=None,
    price_condition=None,
    evidence="277 triple support",
    **kwargs,
):
    return HorizonTrigger(
        horizon=Horizon(horizon),
        direction=direction,
        kind=kind,
        source=EvidenceSource.MARKET,
        condition=condition,
        price_condition=price_condition,
        level=level,
        status=status,
        evidence=evidence,
        **kwargs,
    )


def _view(stance=HorizonStance.HOLD, triggers=()):
    return HorizonView(
        stance=stance,
        confidence="medium",
        thesis="t",
        triggers=list(triggers),
        invalidation="i",
        time_window="days-weeks",
    )


def _decision(
    short=HorizonStance.HOLD,
    mid=HorizonStance.HOLD,
    long=HorizonStance.HOLD,
    short_triggers=(),
    mid_triggers=(),
    long_triggers=(),
    primary=Horizon.MID,
    rating=PortfolioRating.HOLD,
    horizon_note=None,
):
    return PortfolioDecision(
        rating=rating,
        executive_summary="s",
        investment_thesis="t",
        primary_horizon=primary,
        short_term=_view(short, short_triggers),
        mid_term=_view(mid, mid_triggers),
        long_term=_view(long, long_triggers),
        horizon_note=horizon_note,
    )


@pytest.mark.unit
def test_a_minimal_decision_defaults_to_hold_views():
    decision = PortfolioDecision(
        rating=PortfolioRating.HOLD, executive_summary="s", investment_thesis="t"
    )

    assert decision.primary_horizon == Horizon.MID
    assert decision.short_term.stance == HorizonStance.HOLD
    assert decision.long_term.triggers == []


@pytest.mark.unit
def test_a_long_term_sell_on_price_alone_is_downgraded():
    decision = _decision(
        long=HorizonStance.SELL,
        long_triggers=[_trigger(level=276.92, price_condition="below")],
    )

    notes = apply_horizon_policy(decision, FACTS)

    assert decision.long_term.stance == HorizonStance.HOLD
    assert any("Long-term Sell downgraded to Hold" in n for n in notes)


@pytest.mark.unit
def test_a_long_term_sell_with_active_fundamental_evidence_stays():
    decision = _decision(
        long=HorizonStance.SELL,
        long_triggers=[_trigger(kind=TriggerKind.FUNDAMENTAL, condition="FCF regime broken")],
    )

    apply_horizon_policy(decision, FACTS)

    assert decision.long_term.stance == HorizonStance.SELL


@pytest.mark.unit
def test_a_long_term_sell_with_a_confirmed_trend_stays():
    decision = _decision(
        long=HorizonStance.SELL,
        long_triggers=[_trigger(kind=TriggerKind.TREND, condition="200SMA slope down, price below")],
    )

    apply_horizon_policy(decision, FACTS)

    assert decision.long_term.stance == HorizonStance.SELL


@pytest.mark.unit
def test_a_contradicted_trend_trigger_is_invalidated_and_the_sell_downgraded():
    decision = _decision(
        long=HorizonStance.SELL,
        long_triggers=[_trigger(kind=TriggerKind.TREND, condition="200SMA slope down, price below")],
    )
    facts = {**FACTS, "close": 350.0, "sma200_slope_20d_pct": 0.2}

    apply_horizon_policy(decision, facts)

    assert decision.long_term.stance == HorizonStance.HOLD
    assert decision.long_term.triggers[0].status == TriggerStatus.INVALIDATED


@pytest.mark.unit
def test_a_price_trigger_is_rechecked_against_the_close():
    decision = _decision(
        short=HorizonStance.SELL,
        short_triggers=[_trigger(horizon="short", level=276.92, price_condition="below")],
    )

    apply_horizon_policy(decision, FACTS)

    trigger = decision.short_term.triggers[0]
    assert trigger.status == TriggerStatus.PENDING
    assert "284.78" in trigger.status_reason


@pytest.mark.unit
def test_without_facts_the_policy_does_not_downgrade():
    decision = _decision(
        long=HorizonStance.SELL,
        long_triggers=[_trigger(level=276.92, price_condition="below")],
    )

    notes = apply_horizon_policy(decision, None)

    assert decision.long_term.stance == HorizonStance.SELL
    assert any("not independently verified" in n for n in notes)


@pytest.mark.unit
def test_a_divergence_gets_a_note():
    decision = _decision(short=HorizonStance.SELL, long=HorizonStance.HOLD)

    apply_horizon_policy(decision, FACTS)

    assert decision.horizon_note is not None
    assert "does not change the long-term view" in decision.horizon_note


@pytest.mark.unit
def test_horizon_summary_and_rendering():
    decision = _decision(
        short=HorizonStance.SELL,
        mid=HorizonStance.HOLD,
        long=HorizonStance.HOLD,
        horizon_note="tactical sell only",
    )

    assert horizon_summary(decision) == {"short": "Sell", "mid": "Hold", "long": "Hold"}

    rendered = render_pm_decision(decision)
    assert "**Horizon Views**" in rendered
    assert "**Triggers**" in rendered
    assert "**Horizon Divergence**" in rendered
    assert "Short (days-weeks) | Sell" in rendered


@pytest.mark.unit
def test_render_horizon_evidence_prints_the_facts():
    text = render_horizon_evidence(FACTS)

    assert "200SMA 20-day slope" in text
    assert "-0.52" in text
    assert "Latest close" in text


@pytest.mark.unit
def test_build_horizon_facts_computes_from_verified_rows(monkeypatch):
    dates = pd.bdate_range(end="2026-11-06", periods=260)
    frame = pd.DataFrame({
        "Date": dates,
        "Open": 100.0,
        "High": 101.0,
        "Low": 99.0,
        "Close": 100.0 + pd.Series(range(260)) * 0.01,
        "Volume": 1_000_000,
    })
    monkeypatch.setattr(snapshot, "_verified_rows", lambda *a, **k: frame)

    facts = snapshot.build_horizon_facts("AAPL", "2026-11-06")

    assert facts["close"] == pytest.approx(102.59)
    assert facts["sma200"] is not None
    assert facts["sma200_slope_20d_pct"] is not None


@pytest.mark.unit
def test_the_report_header_names_the_horizon_views(tmp_path):
    from tradingagents.reporting import write_report_tree

    state = {
        "trade_date": "2026-11-08",
        "final_trade_decision": "**Rating**: Hold",
        "final_rating": "Hold",
        "horizon_views": {"short": "Sell", "mid": "Hold", "long": "Hold"},
        "primary_horizon": "mid",
        "market_report": "MKT",
    }
    out = write_report_tree(state, "AAPL", tmp_path, html=False)

    text = out.read_text()
    assert "- Horizon views: Short Sell · Mid Hold · Long Hold (primary: mid)" in text
    assert "- Rating: Hold" in text
