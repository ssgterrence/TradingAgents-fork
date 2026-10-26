"""ETF fund metrics in the Yahoo fundamentals output (I-08)."""

import pandas as pd
import pytest

from tradingagents.dataflows import date_window
from tradingagents.dataflows.vendors.yahoo import fundamentals

TODAY = "2026-10-26"

_INFO = {
    "longName": "iShares Semiconductor ETF",
    "quoteType": "ETF",
    "fundFamily": "iShares",
    "legalType": "Exchange Traded Fund",
    "category": "Technology",
    "totalAssets": 48_434_552_832,
    "netExpenseRatio": 0.33,
    "yield": 0.0022,
    "navPrice": 478.50,
    "currency": "USD",
    "marketCap": 48_434_552_832,
    "trailingPE": 28.11,
    "priceToBook": 1.128,
}

_HOLDINGS = pd.DataFrame(
    {
        "Name": ["Intel Corp", "Advanced Micro Devices Inc"],
        "Holding Percent": [0.09591231, 0.09280071],
    },
    index=["INTC", "AMD"],
)


class _Funds:
    top_holdings = _HOLDINGS


class _Ticker:
    def __init__(self, symbol):
        self.symbol = symbol
        self.funds_data = _Funds()


@pytest.mark.unit
def test_etf_fund_metrics_are_rendered(monkeypatch):
    monkeypatch.setattr(date_window, "get_current_date", lambda: TODAY)
    monkeypatch.setattr(fundamentals, "yf_retry", lambda fn: _INFO)
    monkeypatch.setattr(fundamentals.yf, "Ticker", _Ticker)

    out = fundamentals.get_fundamentals("SOXX", TODAY)

    assert "Instrument Type: ETF (fund, not an operating company)" in out
    assert "Fund Family: iShares" in out
    assert "Total Assets: 48434552832 USD" in out
    assert "Net Expense Ratio: 0.33%" in out
    assert "Distribution Yield (TTM): 0.22%" in out
    assert "NAV Price: 478.5 USD" in out
    assert "Top Holdings: INTC Intel Corp 9.6%; AMD Advanced Micro Devices Inc 9.3%" in out
    assert "P/E and P/B above are fund aggregates" in out


@pytest.mark.unit
def test_a_plain_equity_does_not_get_the_etf_block(monkeypatch):
    info = {"longName": "Apple Inc.", "quoteType": "EQUITY", "marketCap": 1000}
    monkeypatch.setattr(date_window, "get_current_date", lambda: TODAY)
    monkeypatch.setattr(fundamentals, "yf_retry", lambda fn: info)
    monkeypatch.setattr(fundamentals.yf, "Ticker", _Ticker)

    out = fundamentals.get_fundamentals("AAPL", TODAY)

    assert "Instrument Type: ETF" not in out
    assert "Top Holdings" not in out
