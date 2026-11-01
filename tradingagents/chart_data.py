"""The structured numbers the HTML report's charts draw from.

The page used to receive only prose, so it could not plot anything without
scraping the model's sentences. This module reads the same vendor data the
agents use (OHLCV from the run's cache, indicators from ``stockstats``) and
returns one JSON-able dict that ``report_html`` can render.

Nothing here invents a number: prices and indicators are computed from the
vendor frame, and the analyst's own levels/scenarios are passed in by the
caller. Build failures are the caller's to swallow, so a missing chart never
stops a report from being written.
"""

from __future__ import annotations

import pandas as pd

from tradingagents.dataflows.vendors.yahoo.ohlcv import load_ohlcv

__all__ = ["build_chart_data"]

# The averages and bands the market analyst reports, in reading order.
_OVERLAYS = (
    ("10 EMA", "close_10_ema", "--accent", "1 0", 1.2),
    ("50 SMA", "close_50_sma", "--muted", "5 3", 1.1),
    ("200 SMA", "close_200_sma", "--ink", "2 2", 1.1),
)


def _round(values, digits: int = 2) -> list[float | None]:
    out = []
    for value in values:
        out.append(None if pd.isna(value) else round(float(value), digits))
    return out


def _fmt(value: float, digits: int = 2) -> str:
    return f"{value:,.{digits}f}".replace("-", "\u2212")


def _fmt_pct(value: float, digits: int = 2, signed: bool = False) -> str:
    sign = ("+" if value > 0 else "\u2212") if signed and value else ("\u2212" if value < 0 else "")
    return f"{sign}{abs(value):,.{digits}f}%"


def build_chart_data(ticker: str, trade_date: str, *, months: int = 7,
                     levels=None, scenarios=None) -> dict:
    """Return ``chart_data`` for ``ticker`` as of ``trade_date``.

    ``levels`` adds the analyst's own prices: ``[{"price": 316.6, "label":
    "10/26 low", "kind": "support"}]``. ``scenarios`` adds the report's own
    odds: ``[{"label": "A · Bounce", "prob": 55, "tone": "--ink"}]``.
    """
    frame = load_ohlcv(ticker, trade_date)
    data = frame[frame["Date"] <= pd.Timestamp(trade_date)].copy()
    data = data[data["Close"].notna()] if "Close" in data else data
    if data.empty:
        raise ValueError(f"no price rows for {ticker} through {trade_date}")

    from stockstats import wrap

    stats = wrap(data)
    for column in ("close_10_ema", "close_50_sma", "close_200_sma", "vwma",
                   "boll", "boll_ub", "boll_lb", "rsi", "macd", "macds", "macdh", "atr"):
        stats[column]  # triggers the lazy calculation

    start = pd.Timestamp(trade_date) - pd.DateOffset(months=months)
    window = pd.DataFrame(stats[stats["Date"] >= start]).reset_index(drop=True)
    if len(window) < 20:  # too little to draw; fall back to everything available
        window = pd.DataFrame(stats.tail(120)).reset_index(drop=True)

    dates = [d.strftime("%Y-%m-%d") for d in window["Date"]]
    close = _round(window["close"])
    volume = [int(v) if not pd.isna(v) else 0 for v in window["volume"]]
    last = close[-1]
    previous = close[-2] if len(close) > 1 else last
    change = (last - previous) / previous * 100 if previous else 0.0

    overlays = [{"name": name, "values": _round(window[column]), "tone": tone,
                 "dash": dash, "width": width}
                for name, column, tone, dash, width in _OVERLAYS]
    bands = {"upper": _round(window["boll_ub"]), "lower": _round(window["boll_lb"]),
             "label": "Bollinger 20,2"}

    # The averages and bands double as levels, tagged by which side price is on.
    derived = [
        (window["close_10_ema"].iloc[-1], "10 EMA"),
        (window["close_50_sma"].iloc[-1], "50 SMA"),
        (window["close_200_sma"].iloc[-1], "200 SMA"),
        (window["vwma"].iloc[-1], "VWMA"),
        (window["boll"].iloc[-1], "BB mid"),
        (window["boll_lb"].iloc[-1], "BB lower"),
    ]
    level_rows = []
    for price, label in derived:
        if pd.isna(price):
            continue
        level_rows.append({"price": round(float(price), 2), "label": label,
                           "kind": "support" if float(price) < last else "resistance"})
    for row in levels or []:
        level_rows.append({"price": float(row["price"]), "label": row.get("label", ""),
                           "kind": row.get("kind", "support")})
    # De-duplicate a caller level that repeats a derived one.
    seen, unique = set(), []
    for row in level_rows:
        key = (round(row["price"], 2), row["label"])
        if key not in seen:
            seen.add(key)
            unique.append(row)

    rsi_last = float(window["rsi"].iloc[-1])
    atr_last = float(window["atr"].iloc[-1])
    year = pd.DataFrame(stats[stats["Date"] >= pd.Timestamp(trade_date) - pd.DateOffset(years=1)])
    high_52w = float(year["high"].max())
    drawdown = (last - high_52w) / high_52w * 100
    sma50 = float(window["close_50_sma"].iloc[-1])
    sma200 = float(window["close_200_sma"].iloc[-1])
    gap = sma50 - sma200
    avg_volume = float(window["volume"].tail(20).mean())
    volume_ratio = volume[-1] / avg_volume if avg_volume else 0

    references = []
    for name, column in (("10 EMA", "close_10_ema"), ("VWMA", "vwma"),
                         ("BB mid", "boll"), ("200 SMA", "close_200_sma"),
                         ("50 SMA", "close_50_sma")):
        value = float(window[column].iloc[-1])
        references.append({"label": name, "value": round((last - value) / value * 100, 2)})

    rsi_label = ("oversold" if rsi_last < 30 else "overbought" if rsi_last > 70
                 else "neutral zone")

    return {
        "as_of": trade_date,
        "ticker": ticker,
        "price": {"dates": dates, "close": close,
                  "high": _round(window["high"]), "low": _round(window["low"]),
                  "volume": volume},
        "overlays": overlays,
        "bands": bands,
        "levels": unique,
        "rsi": {"dates": dates, "values": _round(window["rsi"], 1)},
        "macd": {"dates": dates, "macd": _round(window["macd"]),
                 "signal": _round(window["macds"]),
                 "histogram": _round(window["macdh"])},
        "distances": references,
        "gauge": {"value": round(rsi_last, 1), "label": f"RSI · {rsi_label}"},
        "scenarios": scenarios or [],
        "stats": [
            {"label": "Last close", "value": _fmt(last), "note": dates[-1], "tone": ""},
            {"label": "Day", "value": _fmt_pct(change, 2, signed=True),
             "note": "vs previous close", "tone": "up" if change >= 0 else "down"},
            {"label": "RSI (14)", "value": f"{rsi_last:.1f}", "note": rsi_label,
             "tone": "down" if rsi_last > 70 else "up" if rsi_last < 30 else ""},
            {"label": "ATR (14)", "value": _fmt(atr_last), "note": f"{atr_last / last * 100:.2f}% of price",
             "tone": ""},
            {"label": "From 52w high", "value": _fmt_pct(drawdown, 1, signed=True),
             "note": f"high {_fmt(high_52w)}", "tone": "down" if drawdown < -10 else ""},
            {"label": "50/200 gap", "value": f"{gap:+.2f}".replace("-", "\u2212"),
             "note": f"{gap / sma200 * 100:+.2f}%".replace("-", "\u2212"),
             "tone": "down" if gap < 0 else "up"},
            {"label": "Volume", "value": f"{volume[-1] / 1e6:,.1f}M",
             "note": f"{volume_ratio:.1f}x 20d avg", "tone": ""},
        ],
    }
