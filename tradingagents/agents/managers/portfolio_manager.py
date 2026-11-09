"""Portfolio Manager: synthesises the risk-analyst debate into the final decision.

Uses LangChain's ``with_structured_output`` so the LLM produces a typed
``PortfolioDecision`` directly, in a single call. Its rating is the run's
``final_rating``, and the decision is rendered to markdown as
``final_trade_decision`` for the memory log, CLI display and saved reports.
When a provider does not expose structured output, the agent falls back to
free-text generation and the rating is read from that text.
"""

from __future__ import annotations

from tradingagents.agents.context import (
    get_instrument_context_from_state,
    get_language_instruction,
    get_portfolio_context_from_state,
)
from tradingagents.agents.horizon import (
    apply_horizon_policy,
    horizon_summary,
    render_horizon_evidence,
)
from tradingagents.agents.prompt_rules import HEADLINE_NUMERIC_CLAIM_RULE
from tradingagents.agents.rating import parse_rating
from tradingagents.agents.schemas import PortfolioDecision, render_pm_decision
from tradingagents.agents.structured import NO_EXTERNAL_TOOLS, bind_structured, invoke_structured


def create_portfolio_manager(llm):
    structured_llm = bind_structured(llm, PortfolioDecision, "Portfolio Manager")

    def portfolio_manager_node(state) -> dict:
        instrument_context = get_instrument_context_from_state(state)
        portfolio_context = get_portfolio_context_from_state(state)

        history = state["risk_debate_state"]["history"]
        risk_debate_state = state["risk_debate_state"]
        research_plan = state["investment_plan"]
        trader_plan = state["trader_investment_plan"]

        past_context = state.get("past_context", "")
        lessons_line = (
            f"- Lessons from prior decisions and outcomes:\n{past_context}\n"
            if past_context
            else ""
        )
        horizon_block = render_horizon_evidence(state.get("horizon_facts"))

        prompt = f"""As the Portfolio Manager, synthesize the risk analysts' debate and deliver the final trading decision.

{instrument_context}

{portfolio_context}

---

**Rating Scale** (use exactly one):
- **Buy**: Strong conviction to enter or add to position
- **Overweight**: Favorable outlook, gradually increase exposure
- **Hold**: Maintain current position, no action needed
- **Underweight**: Reduce exposure, take partial profits
- **Sell**: Exit position or avoid entry

**Context:**
- Research Manager's investment plan: **{research_plan}**
- Trader's transaction proposal: **{trader_plan}**
{lessons_line}
**Risk Analysts Debate History:**
{history}

{horizon_block}
---

Ground every conclusion in specific evidence from the analysts. The risk debate always contains conflicting stances; deciding which is stronger is the job, so conflict alone is not a reason to Hold. Commit to the stronger case, sized by how decisively it wins. Choose Hold only when the evidence is still balanced after that weighing, or too thin to support a call; do not force a direction to appear decisive. Weigh the analysts on their merits, independent of speaking order.

## Multi-horizon rules (the result must separate short, mid and long term)

- Give a stance (Buy / Hold / Sell) for each of short_term, mid_term and long_term, with its own thesis, triggers and invalidation.
- **A short-term move does not change mid/long term.** A short-term Sell (e.g. a price drop below support) must NOT force a mid/long-term Sell. Mid/long term change only when their own horizon's trigger becomes active.
- **A long-term Sell requires active long-term evidence** (200SMA slope turning down with price below it, or a fundamental FCF/ROIC regime break, or a structural/regulatory event). Short-term price is not long-term evidence. If no such trigger is active, set long_term to Hold.
- Every trigger must state: horizon, direction (Buy/Sell), kind (price/trend/fundamental/event/sentiment), source, condition, and status (active/pending/invalidated/expired). Only `active` triggers support a stance.
- `primary_horizon` names which horizon the overall `rating` follows; default `mid` unless the mandate is clearly shorter. Keep `rating` directionally consistent with that horizon's stance.
- If the horizons diverge (e.g. short-term Sell, long-term Hold), explain it in `horizon_note`.

## Output

Write these sections, in this order, starting with the rating on its own line:

- **Rating**: exactly one of Buy / Overweight / Hold / Underweight / Sell
- **Horizon Views**: a table of Short / Mid / Long, each with stance (Buy/Hold/Sell), confidence, thesis
- **Triggers**: a table of triggers with their status (active / pending / invalidated / expired) and evidence
- **Executive Summary**: the call and how to act on it
- **Investment Thesis**: the evidence that decided it, and what would change it

{HEADLINE_NUMERIC_CLAIM_RULE}

{NO_EXTERNAL_TOOLS}{get_language_instruction()}"""

        # The typed rating is the decision; the rendered text only carries it.
        # Read back from text, a rating the thesis quotes could replace it.
        decision = invoke_structured(structured_llm, prompt, "Portfolio Manager")
        if decision is not None:
            policy_notes = apply_horizon_policy(decision, state.get("horizon_facts"))
            if policy_notes:
                existing = decision.horizon_note or ""
                decision.horizon_note = (
                    (existing + "\n\n" if existing else "") + "\n".join(f"- {n}" for n in policy_notes)
                )
            final_trade_decision = render_pm_decision(decision)
            final_rating = decision.rating.value
            horizon_views = horizon_summary(decision)
            primary_horizon = decision.primary_horizon.value
        else:
            final_trade_decision = llm.invoke(prompt).content
            final_rating = parse_rating(final_trade_decision)
            horizon_views = {}
            primary_horizon = "mid"

        new_risk_debate_state = {
            "history": risk_debate_state["history"],
            "aggressive_history": risk_debate_state["aggressive_history"],
            "conservative_history": risk_debate_state["conservative_history"],
            "neutral_history": risk_debate_state["neutral_history"],
            "latest_speaker": "Judge",
            "current_aggressive_response": risk_debate_state["current_aggressive_response"],
            "current_conservative_response": risk_debate_state["current_conservative_response"],
            "current_neutral_response": risk_debate_state["current_neutral_response"],
            "count": risk_debate_state["count"],
        }

        return {
            "risk_debate_state": new_risk_debate_state,
            "final_trade_decision": final_trade_decision,
            "final_rating": final_rating,
            "horizon_views": horizon_views,
            "primary_horizon": primary_horizon,
        }

    return portfolio_manager_node
