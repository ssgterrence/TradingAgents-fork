"""Scheduled earnings dates from Yahoo's current calendar, with a past-date guard.

Yahoo's ``Ticker.calendar`` serves the *next* scheduled event; it carries no
historical vintage. A run dated in the past therefore must not be given an event
that had not happened yet, so this module withholds the vendor's answer when the
only event it returns is after the analysis date. Current runs may use it.

The date Yahoo returns is not a confirmed report date: it can be an estimate, it
can be off by a day (a report after the close is often dated to the next
session), and it carries no before-open/after-close timing. Every date served is
therefore labelled unverified, and multiple candidate dates are shown as a
range rather than a single fact.
"""

from __future__ import annotations

from datetime import date, datetime

import yfinance as yf

from tradingagents.dataflows import date_window
from tradingagents.dataflows.symbols import normalize_symbol
from tradingagents.dataflows.vendors.yahoo.common import yf_retry

_UNVERIFIED_LABEL = (
    "source: yfinance, unverified; may be an estimate or off by a day; "
    "timing (before open / after close) unknown."
)
_APPROXIMATE_INSTRUCTION = (
    "treat as approximate; check the company's investor-relations page before trading around it."
)


def _event_dates(calendar) -> list[date]:
    """The calendar's earnings dates as ``date`` objects, de-duplicated and sorted."""
    if not isinstance(calendar, dict):
        return []
    raw = calendar.get("Earnings Date") or []
    if not isinstance(raw, (list, tuple)):
        raw = [raw]
    found: set[date] = set()
    for value in raw:
        if isinstance(value, datetime):
            found.add(value.date())
        elif isinstance(value, date):
            found.add(value)
        else:
            text = value.strip() if isinstance(value, str) else str(value)
            try:
                found.add(datetime.strptime(text[:10], "%Y-%m-%d").date())
            except (TypeError, ValueError):
                continue
    return sorted(found)


def get_earnings_calendar(ticker: str, as_of_date: str | None = None) -> str:
    """Yahoo's next scheduled earnings date, or a withholding notice for a past run.

    ``as_of_date`` is the run's analysis date. A historical run never sees an
    event dated after it; the withheld notice deliberately does not print the
    future date, since naming it would leak the same information.
    """
    canonical = normalize_symbol(ticker)
    calendar = yf_retry(lambda: yf.Ticker(canonical).calendar)
    events = _event_dates(calendar)
    as_of = as_of_date or date_window.get_current_date()

    if date_window.is_historical(as_of):
        run_date = datetime.strptime(as_of, "%Y-%m-%d").date()
        if any(event > run_date for event in events):
            return (
                f"# Earnings Calendar for {canonical}\n"
                f"# Point-in-time as of: {as_of}\n\n"
                "Earnings calendar is withheld for this date. Yahoo's calendar "
                "serves only the next scheduled event, with no historical vintage; "
                "its only event is dated after the analysis date, so serving it "
                "would put post-decision information into the run."
            )
        if not events:
            return (
                f"# Earnings Calendar for {canonical}\n"
                f"# Point-in-time as of: {as_of}\n\n"
                "No earnings date was available from the current vendor calendar. "
                "This is not a statement that the company had no earnings event."
            )

    if not events:
        return (
            f"# Earnings Calendar for {canonical}\n\n"
            "No scheduled earnings date is reported by Yahoo's current calendar. "
            "This is not a statement that the company had no earnings event."
        )

    if len(events) == 1:
        listed = f"Earnings date(s): {events[0].isoformat()}"
    else:
        listed = (
            f"Earnings date range: {events[0].isoformat()} to {events[-1].isoformat()} "
            f"({len(events)} dates reported, not one confirmed date)"
        )
    return (
        f"# Earnings Calendar for {canonical}\n"
        f"# Source: Yahoo Finance current calendar (analysis date {as_of})\n\n"
        f"{listed}\n"
        f"{_UNVERIFIED_LABEL}\n"
        f"{_APPROXIMATE_INSTRUCTION}"
    )
