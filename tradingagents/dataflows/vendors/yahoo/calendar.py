"""Scheduled earnings dates from Yahoo's current calendar, with a past-date guard.

Yahoo's ``Ticker.calendar`` serves the *next* scheduled event; it carries no
historical vintage. A run dated in the past therefore must not be given an event
that had not happened yet, so this module withholds the vendor's answer when the
only event it returns is after the analysis date. Current runs may use it.

The calendar can also lag: right after a report it may still return the quarter
just filed and no next date. ``Ticker.get_earnings_dates``, when Yahoo answers
it, adds the surrounding past and future rows, so the report can name the last
report and, when known, the next one instead of presenting a past date as the
upcoming event.

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


def _as_date(value) -> date | None:
    """One date from whatever a vendor puts in a date slot, or None."""
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    text = value.strip() if isinstance(value, str) else str(value)
    try:
        return datetime.strptime(text[:10], "%Y-%m-%d").date()
    except (TypeError, ValueError):
        return None


def _event_dates(calendar) -> list[date]:
    """The calendar's earnings dates as ``date`` objects, de-duplicated and sorted."""
    if not isinstance(calendar, dict):
        return []
    raw = calendar.get("Earnings Date") or []
    if not isinstance(raw, (list, tuple)):
        raw = [raw]
    found = {parsed for value in raw if (parsed := _as_date(value)) is not None}
    return sorted(found)


def _frame_dates(frame) -> list[date]:
    """The dates in ``get_earnings_dates``' index, when the vendor serves the frame."""
    index = getattr(frame, "index", None)
    if index is None:
        return []
    found = {parsed for value in index if (parsed := _as_date(value)) is not None}
    return sorted(found)


def _extra_dates(canonical: str) -> list[date]:
    """The fuller past-and-future list ``get_earnings_dates`` may serve, else none.

    ``Ticker.calendar`` only names the next event and can be stale: after a
    report it may still return the quarter just filed, leaving no next date.
    ``get_earnings_dates`` carries the surrounding rows on the environments
    where Yahoo answers it. It is optional enrichment, so any failure is a
    missing extra list, not a failed calendar.
    """
    try:
        frame = yf_retry(lambda: yf.Ticker(canonical).get_earnings_dates(limit=12))
    except Exception:  # noqa: BLE001 — optional enrichment must not sink the calendar
        return []
    return _frame_dates(frame)


def get_earnings_calendar(ticker: str, as_of_date: str | None = None) -> str:
    """Yahoo's next scheduled earnings date, or a withholding notice for a past run.

    ``as_of_date`` is the run's analysis date. A historical run never sees an
    event dated after it; the withheld notice deliberately does not print the
    future date, since naming it would leak the same information.
    """
    canonical = normalize_symbol(ticker)
    calendar = yf_retry(lambda: yf.Ticker(canonical).calendar)
    events = sorted(set(_event_dates(calendar)) | set(_extra_dates(canonical)))
    as_of = as_of_date or date_window.get_current_date()
    run_date = datetime.strptime(as_of, "%Y-%m-%d").date()

    if date_window.is_historical(as_of):
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

    header = (
        f"# Earnings Calendar for {canonical}\n"
        f"# Source: Yahoo Finance current calendar (analysis date {as_of})\n\n"
    )
    # A current run may be served a date that has already passed: the vendor's
    # calendar keeps the quarter just reported and not the next one. Do not call
    # that "the earnings date"; name it as the last report and say the next date
    # is unknown, so the reader is not told a past event is upcoming.
    reported = [event for event in events if event < run_date]
    upcoming = [event for event in events if event >= run_date]
    lines = []
    if reported:
        lines.append(f"Last reported: {reported[-1].isoformat()}")
    if upcoming:
        if len(upcoming) == 1:
            lines.append(f"Earnings date(s): {upcoming[0].isoformat()}")
        else:
            lines.append(
                f"Earnings date range: {upcoming[0].isoformat()} to {upcoming[-1].isoformat()} "
                f"({len(upcoming)} dates reported, not one confirmed date)"
            )
    if not upcoming:
        lines.append(
            "Next scheduled: not provided by the vendor calendar. The calendar "
            "currently returns only already-reported dates; this is not a "
            "statement that no future earnings event exists."
        )
    lines.extend([_UNVERIFIED_LABEL, _APPROXIMATE_INSTRUCTION])
    return header + "\n".join(lines)
