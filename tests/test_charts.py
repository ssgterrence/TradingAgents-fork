"""The inline SVG charts: self-contained, labelled, and safe with model text."""

import re

import pytest

from tradingagents import charts

DATES = [f"2026-07-{day:02d}" for day in range(1, 31)]
CLOSE = [100 + day * 0.5 for day in range(30)]
VOLUME = [1_000_000 + day * 10_000 for day in range(30)]


def _price(**overrides):
    options = {
        "dates": DATES, "close": CLOSE, "volume": VOLUME,
        "overlays": [("10 EMA", CLOSE, "--accent", "1 0")],
        "bands": {"upper": [v + 2 for v in CLOSE], "lower": [v - 2 for v in CLOSE]},
        "levels": [(104.0, "10 EMA", "support"), (112.0, "wall", "resistance")],
    }
    options.update(overrides)
    return charts.price_chart(**options)


@pytest.mark.unit
def test_charts_are_inline_svg_with_an_accessible_name():
    svg = _price(title="NVDA price and levels")
    assert svg.startswith("<svg") and svg.endswith("</svg>")
    assert 'role="img"' in svg
    assert "<title>NVDA price and levels</title>" in svg
    assert 'aria-label="NVDA price and levels"' in svg


@pytest.mark.unit
def test_charts_load_nothing_and_run_nothing():
    for svg in (_price(), charts.rsi_panel(DATES, CLOSE),
                charts.macd_panel(DATES, CLOSE, CLOSE, CLOSE),
                charts.gauge(42, label="RSI"), charts.level_ladder([(100, "floor", "support")], 104),
                charts.diverging_bars([("10 EMA", -1.2)]),
                charts.prob_bars([("Base", 60, "--ink")])):
        assert "<script" not in svg.lower()
        assert "<img" not in svg.lower()
        assert "href=" not in svg.lower()


@pytest.mark.unit
def test_chart_text_is_escaped_and_never_prints_nan():
    svg = _price(title='A <b> "quote"', desc="<script>")
    assert "&lt;b&gt;" in svg and "<script>" not in svg
    for bad in ("nan", "NaN", "None"):
        assert bad not in svg


@pytest.mark.unit
def test_a_gauge_clamps_out_of_range_values():
    assert "100.0" in charts.gauge(140, label="high")
    assert "0.0" in charts.gauge(-5, label="low")


@pytest.mark.unit
def test_an_empty_series_renders_nothing():
    assert charts.price_chart([], []) == ""
    assert charts.rsi_panel([], []) == ""
    assert charts.macd_panel([], [], [], []) == ""


@pytest.mark.unit
def test_the_price_chart_labels_every_visible_level():
    svg = _price()
    assert "104.00  10 EMA" in svg
    assert "112.00  wall" in svg
    assert svg.count("<polyline") >= 2


@pytest.mark.unit
def test_no_negative_dimensions_escape():
    svg = _price(volume=None)
    assert not re.search(r'height="-\d', svg)
    assert not re.search(r'width="-\d', svg)


@pytest.mark.unit
def test_the_new_chart_primitives_are_inline_svg():
    svgs = [
        charts.bar_chart(["Q1", "Q2", "Q3"], [1.0, 2.0, 3.0], title="Revenue"),
        charts.line_chart(["Q1", "Q2", "Q3"],
                          [("Gross", [60.0, 61.0, 62.0], "--accent", "1 0")],
                          title="Margins"),
        charts.range_bar(100, 200, 150, markers=[(120, "stop", "--down")],
                         title="52-week range"),
        charts.trade_plan(150, 120, [200], last=160, title="Trade plan"),
        charts.stacked_bar([("Bull", 3, "--up"), ("Bear", 2, "--down")],
                           title="News flow"),
    ]
    for svg in svgs:
        assert svg.startswith("<svg") and svg.endswith("</svg>")
        assert 'role="img"' in svg and "<title>" in svg
        assert "<script" not in svg.lower() and "<img" not in svg.lower()
        assert "href=" not in svg.lower()


@pytest.mark.unit
def test_the_new_charts_tolerate_missing_values_and_empty_input():
    assert charts.bar_chart([], []) == ""
    assert charts.line_chart([], []) == ""
    assert charts.range_bar(100, 100, 100) == ""
    assert charts.trade_plan(100, 100) == ""
    assert charts.stacked_bar([]) == ""
    svg = charts.bar_chart(["Q1", "Q2"], [None, 3.0], title="Revenue")
    assert svg == "" or ("nan" not in svg.lower() and "none" not in svg.lower())


@pytest.mark.unit
def test_the_trade_plan_names_entry_stop_and_target():
    svg = charts.trade_plan(150, 120, [200], last=160, title="Trade plan")
    for label in ("Entry 150.00", "Stop 120.00", "Target 1 200.00"):
        assert label in svg
