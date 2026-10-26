"""The earnings-calendar tool offered to the News and Fundamentals analysts.

Kept in its own module so the upstream ``agents/tools.py`` stays untouched and
the tool can be registered by importing it into each analyst's ``TOOLS`` tuple.
"""

from typing import Annotated

from langchain_core.tools import tool
from langgraph.prebuilt import InjectedState

from tradingagents.dataflows.date_window import as_of
from tradingagents.dataflows.errors import VendorUnavailableError
from tradingagents.dataflows.router import vendor_unavailable
from tradingagents.dataflows.vendors.yahoo.calendar import get_earnings_calendar as _calendar


@tool
def get_earnings_calendar(
    ticker: Annotated[str, InjectedState("company_of_interest")],
    curr_date: Annotated[str, "Current date you are trading at, yyyy-mm-dd"],
    trade_date: Annotated[str, InjectedState("trade_date")] = "",
) -> str:
    """Retrieve the next scheduled earnings date for the instrument.

    Current and future runs use Yahoo's current calendar. A run dated in the
    past is withheld when the only event the vendor serves is after that date,
    because the calendar has no historical vintage. The date is unverified: it
    may be an estimate or off by a day, and its before-open/after-close timing is
    unknown, so present it as approximate.
    """
    try:
        return _calendar(ticker, as_of(curr_date, trade_date))
    except VendorUnavailableError as exc:
        return vendor_unavailable("get_earnings_calendar", exc)
