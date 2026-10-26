"""Earnings calendar: current runs may use it; past runs must not see a future event."""

from datetime import date

import pytest

from tradingagents.agents.analysts import fundamentals_analyst, news_analyst
from tradingagents.agents.tools_earnings import get_earnings_calendar
from tradingagents.dataflows import date_window
from tradingagents.dataflows.vendors.yahoo import calendar as earnings


def _calendar(dates):
    return {"Earnings Date": list(dates)}


@pytest.mark.unit
def test_a_current_run_can_read_the_scheduled_date(monkeypatch):
    monkeypatch.setattr(date_window, "get_current_date", lambda: "2026-10-26")
    monkeypatch.setattr(earnings, "yf_retry", lambda fn: _calendar([date(2026, 10, 29)]))

    out = earnings.get_earnings_calendar("GOOGL", "2026-10-26")

    assert "Earnings date(s): 2026-10-29" in out
    assert "current calendar" in out


@pytest.mark.unit
def test_a_single_date_is_labelled_unverified(monkeypatch):
    monkeypatch.setattr(date_window, "get_current_date", lambda: "2026-10-26")
    monkeypatch.setattr(earnings, "yf_retry", lambda fn: _calendar([date(2026, 10, 29)]))

    out = earnings.get_earnings_calendar("GOOGL", "2026-10-26")

    assert "Earnings date(s): 2026-10-29" in out
    assert "source: yfinance, unverified" in out
    assert "may be an estimate or off by a day" in out
    assert "timing (before open / after close) unknown" in out
    assert "treat as approximate" in out
    assert "investor-relations page" in out


@pytest.mark.unit
def test_two_vendor_dates_are_shown_as_a_range(monkeypatch):
    monkeypatch.setattr(date_window, "get_current_date", lambda: "2026-10-26")
    monkeypatch.setattr(
        earnings,
        "yf_retry",
        lambda fn: _calendar([date(2026, 11, 5), date(2026, 10, 29)]),
    )

    out = earnings.get_earnings_calendar("GOOGL", "2026-10-26")

    assert "Earnings date range: 2026-10-29 to 2026-11-05" in out
    assert "Earnings date(s): 2026-10-29" not in out
    assert "source: yfinance, unverified" in out


@pytest.mark.unit
def test_a_past_run_cannot_see_an_event_after_its_date(monkeypatch):
    monkeypatch.setattr(date_window, "get_current_date", lambda: "2026-10-26")
    monkeypatch.setattr(earnings, "yf_retry", lambda fn: _calendar([date(2026, 10, 29)]))

    out = earnings.get_earnings_calendar("GOOGL", "2026-10-23")

    assert "withheld for this date" in out
    assert "2026-10-29" not in out  # naming the future event would leak it


@pytest.mark.unit
def test_a_past_run_with_no_vendor_event_does_not_claim_there_was_none(monkeypatch):
    monkeypatch.setattr(date_window, "get_current_date", lambda: "2026-10-26")
    monkeypatch.setattr(earnings, "yf_retry", lambda fn: {})

    out = earnings.get_earnings_calendar("GOOGL", "2026-10-23")

    assert "No earnings date was available" in out
    assert "not a statement that the company had no earnings event" in out


@pytest.mark.unit
def test_the_tool_is_offered_to_news_and_fundamentals():
    assert get_earnings_calendar in news_analyst.TOOLS
    assert get_earnings_calendar in fundamentals_analyst.TOOLS
