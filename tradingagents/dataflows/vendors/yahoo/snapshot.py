"""Deterministic market-data verification snapshot.

The market analyst is an LLM that can confabulate exact numbers — citing a
Bollinger band or a "historically validated bounce" that the underlying data
doesn't support (#830). This module computes a ground-truth snapshot (latest
settled OHLCV row on or before the analysis date, common indicators, recent
closes) the analyst is told to treat as the source of truth for any exact
numeric claim. A daily bar is not a close just because the vendor published it;
a current-day session that has not settled is excluded. Deterministic, no LLM
involved.
"""

from __future__ import annotations

from collections.abc import Iterable
from datetime import UTC, datetime, time

import pandas as pd
from stockstats import wrap

from tradingagents.dataflows.errors import NoMarketDataError
from tradingagents.dataflows.symbols import crypto_base, normalize_symbol
from tradingagents.dataflows.vendors.yahoo.common import price_text
from tradingagents.dataflows.vendors.yahoo.ohlcv import load_ohlcv

# A daily bar is not a close just because the vendor published it: Yahoo emits
# a partial candle during the session. The last major cash session (US) closes
# at 21:00 UTC in winter, and the FX day rolls at 22:00 UTC, so 22:30 UTC is
# after both. Crypto has no cash close; its daily bar settles at 00:00 UTC.
_SETTLED_AFTER_UTC = time(22, 30)

# A fixed, common indicator set so the snapshot is the same shape every run.
DEFAULT_SNAPSHOT_INDICATORS: tuple[str, ...] = (
    "close_10_ema", "close_50_sma", "close_200_sma",
    "rsi", "boll", "boll_ub", "boll_lb",
    "macd", "macds", "macdh", "atr",
)


def _now_utc() -> datetime:
    """The clock, isolated so tests can pin a session time."""
    return datetime.now(UTC)


def _is_settled(as_of_date: str, now: datetime | None = None, *, is_crypto: bool = False) -> bool:
    """Whether the ``as_of_date`` daily bar is a final close, not a partial candle.

    A date before today is settled. A cash-market bar dated today is settled
    only after the last major session has closed and the vendor has had a
    moment to publish the final row. Crypto's UTC daily bar is settled only
    once the UTC date has rolled over.
    """
    target = pd.to_datetime(as_of_date).date()
    current = now or _now_utc()
    if current.tzinfo is None:
        current = current.replace(tzinfo=UTC)
    current = current.astimezone(UTC)
    if target < current.date():
        return True
    if target > current.date():
        return False
    if is_crypto:
        return False
    return current.time() >= _SETTLED_AFTER_UTC


def _verified_rows(symbol: str, as_of_date: str, *, now: datetime | None = None) -> pd.DataFrame:
    """OHLCV on or before as_of_date, date-sorted. Raises NoMarketDataError if nothing usable.

    ``load_ohlcv`` already normalizes the Date column and filters out
    look-ahead rows, but we re-apply the cutoff defensively — this is a
    verification path, so it must not trust its input to be pre-filtered.

    A current-day bar is excluded while its session is still open: the vendor
    returns a partial candle whose Close is not the closing price, and row
    inspection cannot tell the two apart. Using the last completed session is
    the only way the snapshot can honestly call itself verified.
    """
    # As reported: this snapshot is quoted by the agents as exact prices, so a
    # gap-filled cell would put the previous session's number under this date.
    data = load_ohlcv(symbol, as_of_date, fill_gaps=False)
    if data is None or data.empty:
        raise NoMarketDataError(symbol, normalize_symbol(symbol), "no price rows")

    df = data.copy()
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date"])
    df = df[df["Date"] <= pd.to_datetime(as_of_date)].sort_values("Date")
    if df.empty:
        raise NoMarketDataError(symbol, normalize_symbol(symbol), f"no price rows on or before {as_of_date}")

    is_crypto = crypto_base(symbol) is not None
    if not _is_settled(as_of_date, now, is_crypto=is_crypto):
        cutoff = pd.to_datetime(as_of_date).normalize()
        df = df[df["Date"] < cutoff]
    if df.empty:
        raise NoMarketDataError(
            symbol, normalize_symbol(symbol), f"no settled price rows on or before {as_of_date}"
        )
    return df


def _fmt(value) -> str:
    if value is None or pd.isna(value):
        return "N/A"
    if isinstance(value, pd.Timestamp):
        return value.strftime("%Y-%m-%d")
    if isinstance(value, bool):
        return str(value)
    if isinstance(value, (int,)):
        return str(value)
    if isinstance(value, float):
        return price_text(value)
    return str(value)


def _num(value):
    """A numeric value or None, so a missing indicator is distinct from zero."""
    if value is None:
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return None if pd.isna(number) else number


def build_horizon_facts(symbol: str, as_of_date: str) -> dict:
    """Deterministic facts for the Portfolio Manager's multi-horizon views.

    The horizon layer must not let a short-term price drop be quoted as a
    long-term trend break, so the PM is given the exact numbers the triggers
    are validated against: close, moving averages, the 200SMA's recent slope,
    the 50/200 relationship, RSI and ATR. Same source as the verified snapshot,
    so the two never disagree.
    """
    df = _verified_rows(symbol, as_of_date)
    stock_df = wrap(df.copy())

    def indicator(name):
        try:
            stock_df[name]  # trigger stockstats to compute it
            return _num(stock_df.iloc[-1][name])
        except Exception:  # noqa: BLE001 — one missing indicator is not fatal
            return None

    close = _num(df.iloc[-1].get("Close"))
    sma50 = indicator("close_50_sma")
    sma200 = indicator("close_200_sma")

    sma200_prev = None
    try:
        stock_df["close_200_sma"]
        if len(stock_df) >= 21:
            sma200_prev = _num(stock_df.iloc[-21]["close_200_sma"])
    except Exception:  # noqa: BLE001
        sma200_prev = None

    slope = None
    if sma200 is not None and sma200_prev:
        slope = (sma200 - sma200_prev) / sma200_prev * 100.0

    price_vs_sma200 = None
    if close is not None and sma200:
        price_vs_sma200 = (close - sma200) / sma200 * 100.0

    atr = indicator("atr")
    atr_pct = None
    if atr is not None and close:
        atr_pct = atr / close * 100.0

    return {
        "latest_date": str(df.iloc[-1]["Date"].date()) if hasattr(df.iloc[-1]["Date"], "date") else str(df.iloc[-1]["Date"]),
        "close": close,
        "ema10": indicator("close_10_ema"),
        "sma50": sma50,
        "sma200": sma200,
        "sma200_prev_20d": sma200_prev,
        "sma200_slope_20d_pct": slope,
        "price_vs_sma200_pct": price_vs_sma200,
        "rsi": indicator("rsi"),
        "atr": atr,
        "atr_pct": atr_pct,
        "vwma": indicator("vwma"),
    }


def build_verified_market_snapshot(
    symbol: str,
    as_of_date: str,
    look_back_days: int = 30,
    indicators: Iterable[str] | None = None,
) -> str:
    """Render a ground-truth snapshot: latest OHLCV row, indicators, recent closes."""
    # `df` keeps the original capitalized OHLCV columns (Open/High/Low/Close/
    # Volume); stockstats `wrap()` lowercases columns and adds indicator
    # columns, so read raw prices from `df` and indicators from `stock_df`.
    is_crypto = crypto_base(symbol) is not None
    df = _verified_rows(symbol, as_of_date)
    stock_df = wrap(df.copy())

    selected = tuple(indicators or DEFAULT_SNAPSHOT_INDICATORS)
    indicator_values: dict[str, str] = {}
    for name in selected:
        try:
            stock_df[name]  # triggers stockstats calculation
            indicator_values[name] = _fmt(stock_df.iloc[-1][name])
        except Exception as exc:  # noqa: BLE001 — one bad indicator shouldn't sink the snapshot
            indicator_values[name] = f"N/A ({type(exc).__name__})"

    latest = df.iloc[-1]
    latest_date = _fmt(latest["Date"])
    window = max(1, min(int(look_back_days), 30))
    recent = df.tail(window)

    lines = [
        f"## Verified market data snapshot for {symbol.upper()}",
        "",
        f"- Requested analysis date: {as_of_date}",
        f"- Latest trading row used: {latest_date}",
        "- Rows after the requested analysis date are excluded before verification.",
    ]
    # A requested date with no settled bar is not necessarily a market holiday:
    # on a trading day before the close (or before the vendor publishes the
    # bar), the latest row is the previous session. Say which case is unknown
    # rather than leaving the model to call a normal session a non-trading day.
    if pd.to_datetime(latest_date).date() != pd.to_datetime(as_of_date).date():
        lines.append(
            f"- Note: no settled bar is available for {as_of_date}; {latest_date} is "
            "the latest completed session. That can mean the requested date is a "
            "weekend or market holiday, or that its session has not closed yet."
        )
        if not _is_settled(as_of_date, is_crypto=is_crypto):
            lines.append(
                f"- Note: the {as_of_date} bar is not a settled close and was excluded; "
                "the row above is the latest close."
            )
    lines += [
        "",
        "### Latest verified OHLCV row",
        "",
        "| Field | Value |",
        "|---|---:|",
    ]
    for field in ("Open", "High", "Low", "Close", "Volume"):
        lines.append(f"| {field} | {_fmt(latest.get(field))} |")

    # Candle anatomy is easy to get wrong from prose: "Close - Low" is the
    # recovery from the low, not the lower shadow. Give the model the exact
    # definitions so a bullish candle is not mislabelled a hammer.
    open_, high, low, close = (_num(latest.get(field)) for field in ("Open", "High", "Low", "Close"))
    if None not in (open_, high, low, close) and high >= low:
        body = abs(close - open_)
        upper = high - max(open_, close)
        lower = min(open_, close) - low
        lines += ["", "### Candle anatomy (derived)", "", "| Field | Value |", "|---|---:|",
                  f"| Body (|Close - Open|) | {_fmt(body)} |",
                  f"| Upper shadow (High - max(Open, Close)) | {_fmt(upper)} |",
                  f"| Lower shadow (min(Open, Close) - Low) | {_fmt(lower)} |"]
        if high > low:
            close_position = (close - low) / (high - low) * 100.0
            lines.append(f"| Close position in range | {close_position:.1f}% |")
        lines.append(
            "Lower shadow is min(Open, Close) - Low, not Close - Low. "
            "Call a candle a hammer only when the lower shadow is at least twice "
            "the body and the upper shadow is small."
        )

    lines += ["", "### Verified technical indicators (latest row)", "",
              "| Indicator | Value |", "|---|---:|"]
    for name, value in indicator_values.items():
        lines.append(f"| {name} | {value} |")

    lines += ["", f"### Recent verified closes (last {len(recent)} rows)", "",
              "| Date | Close |", "|---|---:|"]
    for _, row in recent.iterrows():
        lines.append(f"| {_fmt(row['Date'])} | {_fmt(row.get('Close'))} |")

    lines += [
        "",
        "Use this snapshot as the source of truth for exact OHLCV, price-level, "
        "and indicator-value claims. If another tool output conflicts with it, "
        "flag the discrepancy rather than inventing a reconciled number. Do not "
        "claim historical validation, support/resistance bounces, or exact "
        "percentage moves unless directly supported by tool output with concrete "
        "dates and prices.",
    ]
    return "\n".join(lines)
