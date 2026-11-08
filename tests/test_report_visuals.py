"""The visual summary blocks read the report's own numbers, safely."""

import pytest

from tradingagents import report_visuals as visuals


@pytest.mark.unit
def test_tables_are_read_without_rendering_prose():
    text = (
        "Intro\n\n"
        "| Metric | Value |\n"
        "|---|---:|\n"
        "| Close | 188.10 |\n"
        "| RSI | 47.30 |\n"
    )
    tables = visuals.tables(text)
    assert len(tables) == 1
    assert tables[0].header == ["Metric", "Value"]
    assert tables[0].rows == [["Close", "188.10"], ["RSI", "47.30"]]


@pytest.mark.unit
def test_levels_scenarios_and_the_trade_plan_are_extracted():
    text = (
        "**Resistance ladder:**\n"
        "1. **193.3–196.9** — the decisive band\n"
        "**Support ladder:**\n"
        "1. **184.82** — 10 EMA (first defense)\n"
        "\n"
        "**Base case (neutral, ~55% weight):** drift.\n"
        "**Bearish/caution case (~45% weight):** fail.\n"
    )
    levels = visuals.extract_levels([text])
    assert {"price": 193.3, "label": "the decisive band", "kind": "resistance"} in levels
    assert {"price": 184.82, "label": "10 EMA", "kind": "support"} in levels
    scenarios = visuals.extract_scenarios(text)
    assert [row["prob"] for row in scenarios] == [55, 45]

    plan = visuals.extract_trade_plan({
        "trader_investment_plan": "**Action**: Buy\n**Entry Price**: 188.10 (first tranche)\n"
                                  "**Stop Loss**: 176.70 (below the floor)\n",
        "final_trade_decision": "**Rating**: Overweight\n**Price Target**: 204.5\n",
    })
    assert plan["action"] == "Buy" and plan["rating"] == "Overweight"
    assert plan["entry_price_num"] == 188.10
    assert plan["stop_loss_num"] == 176.70
    assert plan["price_target_num"] == 204.5


@pytest.mark.unit
def test_a_market_scorecard_is_built_from_the_indicator_table():
    text = (
        "## 9. Indicators\n\n"
        "| Indicator | Value | Signal | Why it earns a slot |\n"
        "|---|---:|---|---|\n"
        "| close_10_ema | 184.82 | Short-term repair; price above | first invalidation |\n"
        "| macd | -5.41 | Bearish but improving | pending trigger |\n"
    )
    html = visuals.market_summary(text, {})
    assert 'class="scorecard"' in html
    assert "10 EMA" in html and "MACD" in html
    assert "Short-term repair" in html


@pytest.mark.unit
def test_a_fundamentals_table_becomes_a_chart():
    text = (
        "## 4. Growth\n\n"
        "| Quarter | Revenue | QoQ | YoY | Gross % | Op % | EPS |\n"
        "|---|---:|---:|---:|---:|---:|---:|\n"
        "| Q1 | 2,005 | — | — | 63.6% | 42.8% | $0.64 |\n"
        "| Q2 | 2,205 | +10.0% | — | 65.3% | 44.7% | $0.70 |\n"
        "| Q3 | 2,308 | +4.7% | — | 64.6% | 42.4% | $0.67 |\n"
    )
    html = visuals.fundamentals_summary(text)
    assert 'class="chart' in html
    assert "Quarterly revenue" in html and "Margins" in html


@pytest.mark.unit
def test_report_text_is_escaped_in_visual_cards():
    text = (
        "| Indicator | Value | Signal | Why it earns a slot |\n"
        "|---|---:|---|---|\n"
        "| <script>alert(1)</script> | 1 | <img src=x> | <b>bad</b> |\n"
        "| macd | 2 | neutral | ok |\n"
    )
    html = visuals.market_summary(text, {})
    assert "<script>" not in html and "<img" not in html


@pytest.mark.unit
def test_build_chart_data_returns_empty_when_the_vendor_fails(monkeypatch):
    import tradingagents.chart_data as chart_data

    def boom(*args, **kwargs):
        raise RuntimeError("vendor down")

    monkeypatch.setattr(chart_data, "build_chart_data", boom)
    assert visuals.build_chart_data_for_report("NVDA", {"trade_date": "2026-09-26"}) == {}


@pytest.mark.unit
def test_the_chart_is_reconciled_to_the_report_verified_close():
    data = {
        "price": {"dates": ["2026-10-27", "2026-10-28"],
                  "close": [187.00, 186.72], "volume": [5_000_000, 5_000_000]},
        "overlays": [{"name": "10 EMA", "values": [183.44, 184.00]}],
        "levels": [{"price": 184.00, "label": "10 EMA", "kind": "support"}],
        "rsi": {"dates": ["2026-10-27", "2026-10-28"], "values": [46.0, 46.3]},
        "macd": {"dates": ["2026-10-27", "2026-10-28"],
                 "macd": [-6.0, -5.5], "signal": [-4.5, -4.2], "histogram": [-1.5, -1.3]},
        "distances": [{"label": "10 EMA", "value": 1.0}],
        "gauge": {"value": 46.3, "label": "RSI · neutral zone"},
        "range": {"low": 114.52, "high": 217.41, "last": 186.72},
        "stats": [
            {"label": "Last close", "value": "186.72", "note": "2026-10-28", "tone": ""},
            {"label": "Day", "value": "−0.15%", "note": "vs previous close", "tone": "down"},
            {"label": "RSI (14)", "value": "46.3", "note": "neutral zone", "tone": ""},
        ],
    }
    text = ("**Last verified close:** 188.10\n\n**RSI (47.30):** mid-range.\n\n"
            "| 10 EMA | 184.82 | price above |\n")
    out = visuals.reconcile_chart_data(data, text)
    assert out["reconciled"] is True
    assert out["price"]["close"][-1] == 188.10
    assert out["stats"][0]["value"] == "188.10"
    assert out["stats"][1]["value"] == "+0.59%"
    assert out["gauge"]["value"] == 47.3
    assert out["levels"][0]["price"] == 184.82
