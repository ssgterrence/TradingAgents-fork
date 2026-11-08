"""Vendor failures are recorded and shown, so a thin report says why (#data-quality)."""

import pytest

from tradingagents.dataflows import quality, router
from tradingagents.dataflows.errors import VendorUnavailableError
from tradingagents.reporting import write_report_tree


def _state(entries=None):
    state = {"market_report": "MKT"}
    if entries is not None:
        state["data_quality"] = entries
    return state


@pytest.mark.unit
def test_a_failed_chain_is_recorded_with_the_vendor_error():
    quality.reset()
    quality.record("get_news", "news_data", "failed", ["yfinance"],
                   failures=[("yfinance", "YFDataException")])

    entry = quality.snapshot()[-1]

    assert entry["method"] == "get_news"
    assert entry["status"] == "failed"
    assert entry["failures"] == [{"vendor": "yfinance", "error": "YFDataException"}]


@pytest.mark.unit
def test_a_clean_run_renders_no_data_quality_section():
    quality.reset()
    quality.record("get_stock_data", "core_stock_apis", "ok", ["yfinance"], served_by="yfinance")

    assert quality.render_markdown(quality.snapshot()) == ""


@pytest.mark.unit
def test_the_quality_note_names_the_tool_and_the_failure():
    quality.reset()
    quality.record("get_news", "news_data", "failed", ["yfinance"],
                   failures=[("yfinance", "YFDataException")])

    text = quality.render_markdown(quality.snapshot())

    assert "| get_news | 1 | — | yfinance (YFDataException) |" in text
    assert "a vendor failure, not evidence about the instrument" in text


@pytest.mark.unit
def test_router_records_an_all_vendor_failure(monkeypatch):
    quality.reset()
    monkeypatch.setitem(router.VENDOR_METHODS["get_stock_data"], "yfinance",
                        lambda *a, **k: (_ for _ in ()).throw(VendorUnavailableError("down")))
    monkeypatch.setattr(router, "get_vendor", lambda category, method=None: "yfinance")

    out = router.route_to_vendor("get_stock_data", "AAPL", "2026-01-01", "2026-01-10")

    assert out.startswith("DATA_UNAVAILABLE")
    entry = quality.snapshot()[-1]
    assert entry["status"] == "failed"
    assert ("yfinance", "VendorUnavailableError") in [
        (failure["vendor"], failure["error"]) for failure in entry["failures"]
    ]


@pytest.mark.unit
def test_router_records_a_fallback_as_such(monkeypatch):
    quality.reset()
    monkeypatch.setitem(router.VENDOR_METHODS["get_stock_data"], "yfinance",
                        lambda *a, **k: (_ for _ in ()).throw(VendorUnavailableError("down")))
    monkeypatch.setitem(router.VENDOR_METHODS["get_stock_data"], "alpha_vantage",
                        lambda *a, **k: "OK")
    monkeypatch.setattr(router, "get_vendor",
                        lambda category, method=None: "yfinance,alpha_vantage")

    assert router.route_to_vendor("get_stock_data", "AAPL", "2026-01-01", "2026-01-10") == "OK"

    entry = quality.snapshot()[-1]
    assert entry["status"] == "fallback"
    assert entry["served_by"] == "alpha_vantage"


@pytest.mark.unit
def test_router_marks_a_vendors_internal_search_fallback(monkeypatch):
    quality.reset()
    monkeypatch.setitem(
        router.VENDOR_METHODS["get_news"], "yfinance",
        lambda *a, **k: "## news\n\nNote: the quote feed did not serve these articles; "
                        "they come from Yahoo search.",
    )
    monkeypatch.setattr(router, "get_vendor", lambda category, method=None: "yfinance")

    router.route_to_vendor("get_news", "AAPL", "2026-11-01", "2026-11-08")

    entry = quality.snapshot()[-1]
    assert entry["status"] == "fallback"
    assert entry["failures"] == [{"vendor": "yfinance", "error": "search fallback"}]


@pytest.mark.unit
def test_the_report_shows_data_quality_and_removes_a_stale_note(tmp_path):
    entries = [{
        "method": "get_news", "category": "news_data", "status": "failed",
        "chain": ["yfinance"], "served_by": None,
        "failures": [{"vendor": "yfinance", "error": "YFDataException"}],
    }]

    out = write_report_tree(_state(entries), "AAPL", tmp_path, html=False)

    assert "## Data Quality" in out.read_text()
    assert "get_news" in out.read_text()
    assert (tmp_path / "0_data_quality" / "quality.md").exists()

    # A later clean run must not keep the previous run's warning.
    write_report_tree(_state(), "AAPL", tmp_path, html=False)
    assert not (tmp_path / "0_data_quality" / "quality.md").exists()
