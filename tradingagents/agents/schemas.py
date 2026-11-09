"""Pydantic schemas used by agents that produce structured output.

The framework's primary artifact is still prose: each agent's natural-language
reasoning is what users read in the saved markdown reports and what the
downstream agents read as context.  Structured output is layered onto the
three decision-making agents (Research Manager, Trader, Portfolio Manager)
so that:

- Their outputs follow consistent section headers across runs and providers
- Each provider's native structured-output mode is used (json_schema for
  OpenAI/xAI, response_schema for Gemini, tool-use for Anthropic)
- Schema field descriptions become the model's output instructions, freeing
  the prompt body to focus on context and the rating-scale guidance
- A render helper turns the parsed Pydantic instance back into the same
  markdown shape the rest of the system already consumes, so display,
  memory log, and saved reports keep working unchanged
"""

from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, Field, field_validator

# LLMs sometimes write a placeholder string ("None", "N/A", ...) into an optional
# numeric field instead of omitting it. Coerce those to None so the structured
# call validates instead of erroring (#1058). Pydantic still parses real numeric
# strings ("189.5") to float.
_NULLISH_FLOAT = {"", "none", "n/a", "na", "null", "nil", "-", "tbd", "unknown"}


def _coerce_optional_float(value):
    """Normalise an LLM-written optional numeric field before validation.

    Three shapes show up in practice: a placeholder string ("None", "N/A") in
    place of an omitted value (#1058); a percentage where a price was asked for
    ("15%", #1288); and a human-formatted price ("$1,234.50"). A percentage
    cannot be salvaged into an absolute level -- reading "15%" as 15 would put a
    stop at $15 on a $600 stock -- so it is dropped like a placeholder, leaving
    one bad field to null out instead of failing the whole proposal. A formatted
    price is reduced to its number.

    Anything that is not a single number is dropped the same way. A range
    ("150-160") or a hedge ("around 150") would otherwise reach pydantic, fail
    validation, and discard the whole decision, losing every field the model got
    right along with the price.
    """
    if not isinstance(value, str):
        return value
    text = value.strip()
    if text.lower() in _NULLISH_FLOAT or text.endswith("%"):
        return None
    cleaned = text.replace(",", "").lstrip("$€£¥").strip()
    try:
        return float(cleaned)
    except ValueError:
        return None


# ---------------------------------------------------------------------------
# Shared rating types
# ---------------------------------------------------------------------------


class PortfolioRating(StrEnum):
    """5-tier rating used by the Research Manager and Portfolio Manager."""

    BUY = "Buy"
    OVERWEIGHT = "Overweight"
    HOLD = "Hold"
    UNDERWEIGHT = "Underweight"
    SELL = "Sell"


class TraderAction(StrEnum):
    """3-tier transaction direction used by the Trader.

    The Trader's job is to translate the Research Manager's investment plan
    into a concrete transaction proposal: should the desk execute a Buy, a
    Sell, or sit on Hold this round.  Position sizing and the nuanced
    Overweight / Underweight calls happen later at the Portfolio Manager.
    """

    BUY = "Buy"
    HOLD = "Hold"
    SELL = "Sell"


# ---------------------------------------------------------------------------
# Research Manager
# ---------------------------------------------------------------------------


class ResearchPlan(BaseModel):
    """Structured investment plan produced by the Research Manager.

    Hand-off to the Trader: the recommendation pins the directional view,
    the rationale captures which side of the bull/bear debate carried the
    argument, and the strategic actions translate that into concrete
    instructions the trader can execute against.
    """

    recommendation: PortfolioRating = Field(
        description=(
            "The investment recommendation. Exactly one of Buy / Overweight / "
            "Hold / Underweight / Sell. Conflicting arguments alone are not a "
            "reason to Hold: commit to the stronger side, sized by how "
            "decisively it wins. Choose Hold only when the evidence is still "
            "balanced after weighing, or too thin to support a call."
        ),
    )
    rationale: str = Field(
        description=(
            "Conversational summary of the key points from both sides of the "
            "debate, ending with which arguments led to the recommendation. "
            "Speak naturally, as if to a teammate."
        ),
    )
    strategic_actions: str = Field(
        description=(
            "Concrete steps for the trader to implement the recommendation, "
            "including sizing guidance relative to a standard allocation. The "
            "research team does not see the caller's holdings; the trader and "
            "portfolio manager apply the actual position."
        ),
    )


def render_research_plan(plan: ResearchPlan) -> str:
    """Render a ResearchPlan to markdown for storage and the trader's prompt context."""
    return "\n".join([
        f"**Recommendation**: {plan.recommendation.value}",
        "",
        f"**Rationale**: {plan.rationale}",
        "",
        f"**Strategic Actions**: {plan.strategic_actions}",
    ])


# ---------------------------------------------------------------------------
# Trader
# ---------------------------------------------------------------------------


class TraderProposal(BaseModel):
    """Structured transaction proposal produced by the Trader.

    The trader reads the Research Manager's investment plan and the analyst
    reports, then turns them into a concrete transaction: what action to
    take, the reasoning that justifies it, and the practical levels for
    entry, stop-loss, and sizing.
    """

    action: TraderAction = Field(
        description="The transaction direction. Exactly one of Buy / Hold / Sell.",
    )
    reasoning: str = Field(
        description=(
            "The case for this action, anchored in the analysts' reports and "
            "the research plan. Two to four sentences."
        ),
    )
    entry_price: float | None = Field(
        default=None,
        description=(
            "Optional entry price target as an absolute number in the instrument's "
            "quote currency (e.g. 189.5), never a percentage or a range. Omit it "
            "if you cannot state a specific level."
        ),
    )
    stop_loss: float | None = Field(
        default=None,
        description=(
            "Optional stop-loss as an absolute price in the instrument's quote "
            "currency (e.g. 172.0), never a percentage. Convert a percentage "
            "distance to the price level it implies, or omit it."
        ),
    )
    position_sizing: str | None = Field(
        default=None,
        description="Optional sizing guidance, e.g. '5% of portfolio'.",
    )

    @field_validator("entry_price", "stop_loss", mode="before")
    @classmethod
    def _nullish_float_to_none(cls, v):
        return _coerce_optional_float(v)


def render_trader_proposal(proposal: TraderProposal) -> str:
    """Render a TraderProposal to markdown.

    The trailing ``FINAL TRANSACTION PROPOSAL: **BUY/HOLD/SELL**`` line is
    preserved for backward compatibility with the analyst stop-signal text
    and any external code that greps for it.
    """
    parts = [
        f"**Action**: {proposal.action.value}",
        "",
        f"**Reasoning**: {proposal.reasoning}",
    ]
    # Named even when absent, so a reader can tell a level the trader chose not
    # to give from one the schema never asked for. A Hold places no new entry,
    # so "not provided" there would read as a gap rather than as "not applicable".
    for label, value in (("Entry Price", proposal.entry_price),
                         ("Stop Loss", proposal.stop_loss),
                         ("Position Sizing", proposal.position_sizing)):
        if value is not None and value != "":
            shown = value
        elif label == "Entry Price" and proposal.action.value == "Hold":
            shown = "N/A (Hold places no new entry; an existing position stays as is)"
        else:
            shown = "not provided"
        parts.extend(["", f"**{label}**: {shown}"])
    parts.extend([
        "",
        f"FINAL TRANSACTION PROPOSAL: **{proposal.action.value.upper()}**",
    ])
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Multi-horizon views (Portfolio Manager)
# ---------------------------------------------------------------------------


class Horizon(StrEnum):
    """A view's time horizon; the overall rating follows ``primary_horizon``."""

    SHORT = "short"
    MID = "mid"
    LONG = "long"


class HorizonStance(StrEnum):
    """Direction within one horizon. Three tiers keep each horizon readable."""

    BUY = "Buy"
    HOLD = "Hold"
    SELL = "Sell"


class TriggerDirection(StrEnum):
    """A trigger is a condition that would justify a Buy or a Sell."""

    BUY = "Buy"
    SELL = "Sell"


class TriggerKind(StrEnum):
    """What sort of evidence a trigger is, so short-term price is told from long-term trend."""

    PRICE = "price"
    TREND = "trend"
    FUNDAMENTAL = "fundamental"
    EVENT = "event"
    SENTIMENT = "sentiment"


class TriggerStatus(StrEnum):
    """Whether a trigger is satisfied now, or only a level to watch."""

    ACTIVE = "active"
    PENDING = "pending"
    INVALIDATED = "invalidated"
    EXPIRED = "expired"


class EvidenceSource(StrEnum):
    """Which analyst report the trigger's evidence came from."""

    MARKET = "market"
    FUNDAMENTALS = "fundamentals"
    NEWS = "news"
    SENTIMENT = "sentiment"
    RISK_DEBATE = "risk_debate"
    LESSON = "lesson"


class HorizonTrigger(BaseModel):
    """One condition that supports (or, if invalidated, fails to support) a view.

    ``price_condition`` + ``level`` let the policy verify a price trigger against
    the latest close, so a model cannot call a not-yet-reached level "active".
    """

    horizon: Horizon
    direction: TriggerDirection
    kind: TriggerKind
    source: EvidenceSource
    condition: str
    price_condition: Literal["above", "below"] | None = None
    level: float | None = None
    status: TriggerStatus
    status_reason: str | None = None
    evidence: str
    invalid_if: str | None = None

    @field_validator("level", mode="before")
    @classmethod
    def _coerce_level(cls, value):
        return _coerce_optional_float(value)


class HorizonView(BaseModel):
    """The call for one horizon, plus the triggers that back it and what breaks it."""

    stance: HorizonStance
    confidence: Literal["low", "medium", "high"]
    thesis: str
    triggers: list[HorizonTrigger] = Field(default_factory=list, max_length=3)
    invalidation: str
    time_window: str


def _default_horizon_view() -> HorizonView:
    """A neutral view for runs/models that do not fill the horizon layer."""
    return HorizonView(
        stance=HorizonStance.HOLD,
        confidence="low",
        thesis="",
        triggers=[],
        invalidation="",
        time_window="",
    )


# ---------------------------------------------------------------------------
# Portfolio Manager
# ---------------------------------------------------------------------------


class PortfolioDecision(BaseModel):
    """Structured output produced by the Portfolio Manager.

    The model fills every field as part of its primary LLM call; no separate
    extraction pass is required. Field descriptions double as the model's
    output instructions, so the prompt body only needs to convey context and
    the rating-scale guidance.
    """

    rating: PortfolioRating = Field(
        description=(
            "The final position rating. Exactly one of Buy / Overweight / Hold / "
            "Underweight / Sell, picked based on the analysts' debate. "
            "Conflicting arguments alone are not a reason to Hold: commit to the "
            "stronger side, sized by how decisively it wins. Choose Hold only "
            "when the evidence is still balanced after weighing, or too thin to "
            "support a call."
        ),
    )
    executive_summary: str = Field(
        description=(
            "A concise action plan covering entry strategy, position sizing, "
            "key risk levels, and time horizon. Two to four sentences."
        ),
    )
    investment_thesis: str = Field(
        description=(
            "Detailed reasoning anchored in specific evidence from the analysts' "
            "debate. If prior lessons are referenced in the prompt context, "
            "incorporate them; otherwise rely solely on the current analysis."
        ),
    )
    price_target: float | None = Field(
        default=None,
        description="Optional target price in the instrument's quote currency.",
    )
    time_horizon: str | None = Field(
        default=None,
        description="Optional recommended holding period, e.g. '3-6 months'.",
    )
    primary_horizon: Horizon = Field(
        default=Horizon.MID,
        description=(
            "Which horizon the overall `rating` follows. Exactly one of short / mid / long. "
            "Default to mid for a general investor; use short only for a trading mandate. "
            "The `rating` must be directionally consistent with that horizon's stance."
        ),
    )
    short_term: HorizonView = Field(
        default_factory=_default_horizon_view,
        description=(
            "Short-term view (days to weeks). Price action, 10EMA/VWMA, RSI, ATR, volume and "
            "near-term events decide it. A short-term Sell does NOT change the mid/long view."
        ),
    )
    mid_term: HorizonView = Field(
        default_factory=_default_horizon_view,
        description=(
            "Mid-term view (weeks to months). 50SMA, earnings/capex trends, sector rotation and "
            "1-6 month events decide it."
        ),
    )
    long_term: HorizonView = Field(
        default_factory=_default_horizon_view,
        description=(
            "Long-term view (quarters to years). 200SMA slope and price position, revenue/FCF/ROIC "
            "regime, and structural/competitive changes decide it. A long-term Sell requires an "
            "active long-term trend/fundamental/event trigger; short-term price evidence is not enough."
        ),
    )
    horizon_note: str | None = Field(
        default=None,
        description=(
            "Explain any divergence between the horizons (e.g. short-term Sell while long-term "
            "Hold), and why one horizon's call does not override another without its own trigger."
        ),
    )

    @field_validator("price_target", mode="before")
    @classmethod
    def _nullish_float_to_none(cls, v):
        return _coerce_optional_float(v)


_HORIZON_LABELS = {
    "short": "Short (days-weeks)",
    "mid": "Mid (weeks-months)",
    "long": "Long (quarters-years)",
}


def _horizon_table(decision: PortfolioDecision) -> str:
    rows = []
    for key in ("short", "mid", "long"):
        view = getattr(decision, f"{key}_term")
        rows.append(
            f"| {_HORIZON_LABELS[key]} | {view.stance.value} | "
            f"{view.confidence.capitalize()} | {view.time_window or '—'} | {view.thesis or '—'} |"
        )
    return "\n".join([
        "| Horizon | Stance | Confidence | Time Window | Thesis |",
        "|---|---|---|---|---|",
        *rows,
    ])


def _trigger_table(decision: PortfolioDecision) -> str:
    rows = []
    for key in ("short", "mid", "long"):
        for trigger in getattr(decision, f"{key}_term").triggers:
            status = trigger.status.value
            if trigger.status_reason:
                status += f" ({trigger.status_reason})"
            condition = trigger.condition or "—"
            if trigger.level is not None:
                condition += f" @ {trigger.level}"
            rows.append(
                f"| {key} | {trigger.direction.value} | {condition} | "
                f"{status} | {trigger.evidence or '—'} |"
            )
    header = "| Horizon | Direction | Trigger | Status | Evidence |\n|---|---|---|---|---|"
    if not rows:
        rows = ["| — | — | no triggers | — | — |"]
    return "\n".join([header, *rows])


def render_pm_decision(decision: PortfolioDecision) -> str:
    """Render a PortfolioDecision back to the markdown shape the rest of the system expects.

    Memory log, CLI display, and saved report files all read this markdown,
    so the rendered output preserves the exact section headers (``**Rating**``,
    ``**Executive Summary**``, ``**Investment Thesis**``) that downstream
    parsers and the report writers already handle.
    """
    parts = [
        f"**Rating**: {decision.rating.value}",
        "",
        f"**Executive Summary**: {decision.executive_summary}",
        "",
        f"**Investment Thesis**: {decision.investment_thesis}",
        "",
        "**Horizon Views**",
        "",
        _horizon_table(decision),
        "",
        "**Triggers**",
        "",
        _trigger_table(decision),
    ]
    if decision.horizon_note:
        parts += ["", "**Horizon Divergence**", "", decision.horizon_note]
    # Named even when absent: a missing line reads as a field nobody asked for,
    # so a reader cannot tell "no target" from "target not reported".
    target = decision.price_target if decision.price_target is not None else "not provided"
    parts.extend(["", f"**Price Target**: {target}"])
    parts.extend(["", f"**Time Horizon**: {decision.time_horizon or 'not provided'}"])
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Sentiment Analyst
# ---------------------------------------------------------------------------


class SentimentBand(StrEnum):
    """Discrete sentiment direction produced by the Sentiment Analyst.

    Six tiers keep the signal granular enough to be actionable while remaining
    small enough for every provider to map reliably from its JSON output.
    """

    BULLISH = "Bullish"
    MILDLY_BULLISH = "Mildly Bullish"
    NEUTRAL = "Neutral"
    MIXED = "Mixed"
    MILDLY_BEARISH = "Mildly Bearish"
    BEARISH = "Bearish"


class SentimentReport(BaseModel):
    """Structured sentiment report produced by the Sentiment Analyst.

    Replaces the previous free-form prose output so downstream consumers
    (dashboards, audit logs, PDF renderers, other agents) can read
    ``overall_band`` and ``overall_score`` without maintaining fragile regex
    fallbacks that drift with every model release. ``narrative`` preserves the
    rich source-by-source analysis; ``render_sentiment_report`` prepends a
    deterministic header so the saved report stays human-readable.
    """

    overall_band: SentimentBand = Field(
        description=(
            "Overall sentiment direction. Exactly one of: "
            "Bullish / Mildly Bullish / Neutral / Mixed / Mildly Bearish / Bearish. "
            "Use Mixed when sources point in clearly different directions. "
            "Use Neutral only when all sources are genuinely silent or non-committal."
        ),
    )
    overall_score: float = Field(
        ge=0.0,
        le=10.0,
        description=(
            "Numeric sentiment intensity on a 0–10 scale. "
            "0 = maximally bearish, 5 = neutral, 10 = maximally bullish. "
            "Guideline for consistency with overall_band: "
            "Bullish ~6.5–10, Mildly Bullish ~5.5–6.4, Neutral/Mixed ~4.5–5.5, "
            "Mildly Bearish ~3.5–4.4, Bearish ~0–3.4. "
            "Only the 0–10 bounds are enforced."
        ),
    )
    confidence: Literal["low", "medium", "high"] = Field(
        description=(
            "Confidence in the assessment based on data quality and sample size. "
            "Use 'low' when one or more sources returned a placeholder or fewer "
            "than 5 data points; 'medium' when data is present but sparse; "
            "'high' when all three sources returned substantive data."
        ),
    )
    narrative: str = Field(
        description=(
            "Full sentiment report covering, in order: "
            "(1) source-by-source breakdown with specific evidence (cite message "
            "counts, ratios, notable posts); "
            "(2) cross-source divergences and alignments; "
            "(3) dominant narrative themes; "
            "(4) catalysts and risks surfaced by the data; "
            "(5) a markdown table summarising key sentiment signals, their "
            "direction, source, and supporting evidence. "
            "Keep it informative and substantive: develop each section thoroughly "
            "with concrete evidence so every point adds new signal for the trader."
        ),
    )


def render_sentiment_report(report: SentimentReport) -> str:
    """Render a SentimentReport to the markdown shape the rest of the system expects.

    The structured header (band + score + confidence) is prepended to the
    narrative so the saved report is both human-readable and machine-parseable
    without regex.
    """
    return "\n".join([
        f"**Overall Sentiment:** **{report.overall_band.value}** "
        f"(Score: {report.overall_score:.1f}/10)",
        f"**Confidence:** {report.confidence.capitalize()}",
        "",
        report.narrative,
    ])
