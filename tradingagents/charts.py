"""Inline SVG charts for the self-contained HTML report.

Every function returns one ``<svg>`` element: no script, no remote asset, no
``<img>``. Colours come from the page's CSS custom properties, so the charts
follow the light, dark and print themes without a second palette. The numbers
are drawn by Python from the run's tool output, never parsed out of prose.
"""

from __future__ import annotations

import math
from datetime import datetime
from html import escape

__all__ = [
    "price_chart",
    "rsi_panel",
    "macd_panel",
    "gauge",
    "level_ladder",
    "diverging_bars",
    "prob_bars",
]


# --------------------------------------------------------------------------- #
# primitives
# --------------------------------------------------------------------------- #

def _num(value: float, digits: int = 2) -> str:
    """A price or indicator value, with a true minus sign and thin grouping."""
    text = f"{value:,.{digits}f}"
    return text.replace("-", "\u2212")


def _pct(value: float, digits: int = 1) -> str:
    return f"{_num(value, digits)}%"


def _signed_pct(value: float, digits: int = 1) -> str:
    sign = "+" if value > 0 else ("\u2212" if value < 0 else "")
    return f"{sign}{_num(abs(value), digits)}%"


def _date(text: str) -> str:
    try:
        parsed = datetime.strptime(text[:10], "%Y-%m-%d")
    except ValueError:
        return text[:10]
    return f"{parsed:%b} {parsed.day}"


def _text(x: float, y: float, value: str, *, anchor: str = "start",
          size: float = 10, weight: int | None = None, tone: str | None = None,
          extra: str = "") -> str:
    style = f"font:{weight or 400} {size}px var(--sans)"
    if tone:
        style += f";fill:var({tone})"
    return (f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" class="c-axis" '
            f'style="{style}"{extra}>{escape(value)}</text>')


def _line(x1, y1, x2, y2, *, cls: str, extra: str = "") -> str:
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'class="{cls}"{extra}/>')


def _polyline(points, *, cls: str, width: float = 1.6, extra: str = "") -> str:
    path = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
    return (f'<polyline points="{path}" class="{cls}" fill="none" '
            f'stroke-width="{width}"{extra}/>')


def _domain(values, pad: float = 0.06) -> tuple[float, float]:
    clean = [float(v) for v in values if v is not None and not math.isnan(float(v))]
    lo, hi = min(clean), max(clean)
    if hi == lo:
        hi = lo + 1
    span = (hi - lo) * pad
    return lo - span, hi + span


def _ticks(lo: float, hi: float, count: int = 4) -> list[float]:
    step = (hi - lo) / count
    return [lo + step * i for i in range(count + 1)]


def _label_rows(items, top: float, bottom: float, gap: float = 13.0):
    """Place right-hand labels without overlap: sort, spread, then pull back up."""
    rows = sorted(items, key=lambda item: item[0])
    placed = []
    for actual, payload in rows:
        y = max(actual, top) if not placed else max(actual, placed[-1][0] + gap)
        placed.append([y, actual, payload])
    if placed:
        overflow = placed[-1][0] - bottom
        if overflow > 0:
            for row in placed:
                row[0] -= overflow
        underflow = top - placed[0][0]
        if underflow > 0:
            for row in placed:
                row[0] += underflow
    return [(row[0], row[1], row[2]) for row in placed]


# --------------------------------------------------------------------------- #
# price
# --------------------------------------------------------------------------- #

def price_chart(dates: list[str], close: list[float], *, high=None, low=None,
                volume=None, overlays=(), bands: dict | None = None,
                levels=(), width: int = 780, height: int = 430,
                title: str = "Price", desc: str = "") -> str:
    """Close line with averages, an optional band, volume, and labelled levels.

    ``overlays`` is a sequence of ``(name, values, tone, dash)``; ``bands`` is
    ``{"upper": [...], "lower": [...], "label": "Bollinger 20,2"}``; ``levels``
    is a sequence of ``(price, short name, "support" | "resistance")``.
    """
    n = len(close)
    if n < 2:
        return ""
    left, right = 52, 106
    top = 30 if overlays else 16
    bottom = 24
    vol_h = 58 if volume else 0
    gap = 12
    plot_right = width - right
    price_bottom = height - bottom - (vol_h + gap if volume else 0)
    plot_w = plot_right - left
    def x(index):
        return left + index * plot_w / (n - 1)

    candidates = list(close) + [v for _, values, _, _ in overlays for v in values]
    if bands:
        candidates += list(bands.get("upper") or []) + list(bands.get("lower") or [])
    raw_lo, raw_hi = _domain(candidates, pad=0.0)
    level_values = [p for p, _, _ in levels if raw_lo - (raw_hi - raw_lo) * 0.5
                    <= p <= raw_hi + (raw_hi - raw_lo) * 0.5]
    lo, hi = _domain(candidates + level_values)
    def y(value):
        return price_bottom - (value - lo) / (hi - lo) * (price_bottom - top)

    parts = []
    # Grid and price axis.
    for value in _ticks(lo, hi, 4):
        parts.append(_line(left, y(value), plot_right, y(value), cls="c-grid"))
        parts.append(_text(left - 8, y(value) + 3.5, _num(value), anchor="end"))

    # The band sits under the lines, as a wash rather than a second line.
    if bands and bands.get("upper") and bands.get("lower"):
        upper = list(bands["upper"])
        lower = list(bands["lower"])
        complete = all(v is not None and not math.isnan(float(v)) for v in upper + lower)
        if complete:
            area = " ".join(f"{x(i):.1f},{y(v):.1f}" for i, v in enumerate(upper))
            area += " " + " ".join(f"{x(i):.1f},{y(v):.1f}"
                                   for i, v in reversed(list(enumerate(lower))))
            parts.append(f'<polygon points="{area}" class="c-band"/>')

    # Key levels: dashed rules, labelled on the right.
    label_items = []
    for price, name, kind in levels:
        if not lo <= price <= hi:
            continue
        cls = "c-level-support" if kind == "support" else "c-level-resistance"
        parts.append(_line(left, y(price), plot_right, y(price), cls=cls))
        label_items.append((y(price), f"{_num(price)}  {name}"))
    label_items.append((y(close[-1]), f"{_num(close[-1])}  last"))

    # Volume, coloured by the day's direction.
    if volume:
        vtop = price_bottom + gap
        vbottom = height - bottom
        inner_top = vtop + 13  # headroom for the volume label
        vmax = max(float(v) for v in volume if v) or 1.0
        bar_w = max(1.2, plot_w / n * 0.62)
        for i, value in enumerate(volume):
            if not value:
                continue
            h = (float(value) / vmax) * (vbottom - inner_top)
            cls = "c-volume-up" if i == 0 or close[i] >= close[i - 1] else "c-volume-down"
            parts.append(f'<rect x="{x(i) - bar_w / 2:.1f}" y="{vbottom - h:.1f}" '
                         f'width="{bar_w:.1f}" height="{h:.1f}" class="{cls}"/>')
        recent = [float(v) for v in volume[-20:] if v]
        avg = sum(recent) / len(recent) if recent else 0
        last_volume = next((v for v in reversed(volume) if v), 0)
        parts.append(_text(left, vtop + 9,
                           f"Volume · last {last_volume / 1e6:,.1f}M · 20d avg {avg / 1e6:,.1f}M",
                           size=9, tone="--muted"))

    # Price and averages.
    parts.append(_polyline([(x(i), y(v)) for i, v in enumerate(close)],
                           cls="c-price", width=1.7))
    for _name, values, tone, dash in overlays:
        points = [(x(i), y(v)) for i, v in enumerate(values)
                  if v is not None and not math.isnan(float(v))]
        parts.append(_polyline(points, cls="c-overlay", width=1.2,
                               extra=f' stroke="var({tone})" stroke-dasharray="{dash}"'))

    # Legend above the plot.
    if overlays:
        cursor = left
        for name, _values, tone, dash in overlays:
            parts.append(_line(cursor, 14, cursor + 16, 14, cls="c-overlay",
                               extra=f' stroke="var({tone})" stroke-dasharray="{dash}"'))
            parts.append(_text(cursor + 20, 17, name, size=9, tone="--muted"))
            cursor += 26 + len(name) * 5.4

    # Date axis.
    for i in sorted({0, n // 4, n // 2, 3 * n // 4, n - 1}):
        parts.append(_text(x(i), height - 7, _date(dates[i]), anchor="middle", size=9))

    # Last close marker.
    parts.append(f'<circle cx="{x(n - 1):.1f}" cy="{y(close[-1]):.1f}" r="2.6" class="c-dot"/>')

    # Right-hand labels, spread so a tight cluster such as 339.81/340.88/341.45 reads.
    for label_y, _actual, text in _label_rows(label_items, top + 4, price_bottom - 4):
        parts.append(_line(plot_right + 2, label_y, plot_right + 6, label_y, cls="c-grid"))
        parts.append(_text(plot_right + 9, label_y + 3.5, text, size=9))

    return _svg(width, height, "".join(parts), title, desc)


# --------------------------------------------------------------------------- #
# indicator panels
# --------------------------------------------------------------------------- #

def rsi_panel(dates: list[str], values: list[float], *, width: int = 780,
              height: int = 118, period: int = 14) -> str:
    n = len(values)
    if n < 2:
        return ""
    left, right, top, bottom = 52, 40, 12, 22
    plot_w = width - left - right
    def x(index):
        return left + index * plot_w / (n - 1)
    def y(value):
        return top + (100 - value) / 100 * (height - top - bottom)
    last = next((v for v in reversed(values) if v is not None), None)

    parts = []
    # Oversold and overbought washes.
    parts.append(f'<rect x="{left}" y="{top}" width="{plot_w}" height="{y(70) - top:.1f}" '
                 f'class="c-zone-down"/>')
    parts.append(f'<rect x="{left}" y="{y(30):.1f}" width="{plot_w}" '
                 f'height="{height - bottom - y(30):.1f}" class="c-zone-up"/>')
    for level, label in ((30, "30"), (50, "50"), (70, "70")):
        dash = "2 3" if level == 50 else "4 3"
        parts.append(_line(left, y(level), width - right, y(level), cls="c-level",
                           extra=f' stroke-dasharray="{dash}"'))
        parts.append(_text(left - 8, y(level) + 3.5, label, anchor="end"))
    for i in sorted({0, n // 4, n // 2, 3 * n // 4, n - 1}):
        parts.append(_text(x(i), height - 6, _date(dates[i]), anchor="middle", size=9))
    points = [(x(i), y(v)) for i, v in enumerate(values) if v is not None]
    parts.append(_polyline(points, cls="c-indicator", width=1.4))
    if last is not None:
        parts.append(f'<circle cx="{x(n - 1):.1f}" cy="{y(last):.1f}" r="2.4" '
                     f'class="c-indicator-dot"/>')
        parts.append(_text(x(n - 1) - 6, max(y(last) - 7, top + 9), _num(last, 1),
                           anchor="end", size=9, weight=600, tone="--accent",
                           extra=' paint-order="stroke" stroke="var(--paper)" stroke-width="3"'))
    title = f"RSI ({period})"
    desc = f"Relative strength index over {n} sessions; last {last:.1f}." if last else title
    return _svg(width, height, "".join(parts), title, desc)


def macd_panel(dates: list[str], macd: list[float], signal: list[float],
               histogram: list[float], *, width: int = 780, height: int = 132) -> str:
    n = len(macd)
    if n < 2:
        return ""
    left, right, top, bottom = 52, 40, 12, 22
    plot_w = width - left - right
    def x(index):
        return left + index * plot_w / (n - 1)
    values = [v for series in (macd, signal, histogram) for v in series if v is not None]
    extent = max(abs(v) for v in values) or 1.0
    mid = top + (height - top - bottom) / 2
    half = (height - top - bottom) / 2
    def y(value):
        return mid - (value / extent) * half * 0.92

    parts = [_line(left, mid, width - right, mid, cls="c-level"),
             _text(left - 8, mid + 3.5, "0", anchor="end")]
    bar_w = max(1.0, plot_w / n * 0.55)
    for i, value in enumerate(histogram):
        if value is None:
            continue
        cls = "c-volume-up" if value >= 0 else "c-volume-down"
        y0, y1 = y(0), y(value)
        parts.append(f'<rect x="{x(i) - bar_w / 2:.1f}" y="{min(y0, y1):.1f}" '
                     f'width="{bar_w:.1f}" height="{abs(y1 - y0):.1f}" class="{cls}"/>')
    parts.append(_polyline([(x(i), y(v)) for i, v in enumerate(macd) if v is not None],
                           cls="c-indicator", width=1.3))
    parts.append(_polyline([(x(i), y(v)) for i, v in enumerate(signal) if v is not None],
                           cls="c-overlay", width=1.1,
                           extra=' stroke="var(--muted)" stroke-dasharray="4 3"'))
    for i in sorted({0, n // 4, n // 2, 3 * n // 4, n - 1}):
        parts.append(_text(x(i), height - 6, _date(dates[i]), anchor="middle", size=9))
    last_macd = next((v for v in reversed(macd) if v is not None), 0.0)
    last_signal = next((v for v in reversed(signal) if v is not None), 0.0)
    parts.append(_text(x(n - 1) - 6, max(y(last_macd) - 7, top + 9), _num(last_macd),
                       anchor="end", size=9, weight=600, tone="--accent",
                       extra=' paint-order="stroke" stroke="var(--paper)" stroke-width="3"'))
    title = "MACD (12,26,9)"
    desc = (f"MACD {last_macd:.2f}, signal {last_signal:.2f}, "
            f"histogram {(last_macd - last_signal):.2f}.")
    return _svg(width, height, "".join(parts), title, desc)


# --------------------------------------------------------------------------- #
# gauges, ladders, bars
# --------------------------------------------------------------------------- #

def _polar(cx, cy, r, degrees):
    angle = math.radians(180 - degrees * 1.8)
    return cx + r * math.cos(angle), cy - r * math.sin(angle)


def _arc(cx, cy, r, start, end):
    x0, y0 = _polar(cx, cy, r, start)
    x1, y1 = _polar(cx, cy, r, end)
    large = 1 if end - start > 50 else 0
    return f"M {x0:.1f} {y0:.1f} A {r} {r} 0 {large} 1 {x1:.1f} {y1:.1f}"


def gauge(value: float, *, label: str = "", width: int = 260, height: int = 150,
          title: str = "Gauge") -> str:
    """A semicircular 0-100 gauge, for RSI or another bounded score."""
    value = max(0.0, min(100.0, float(value)))
    cx, cy, r = width / 2, height - 24, min(width / 2 - 18, height - 40)
    parts = [f'<path d="{_arc(cx, cy, r, 0, 100)}" class="c-gauge-track" fill="none" '
             f'stroke-width="13" stroke-linecap="round"/>']
    for start, end, cls in ((0, 30, "c-gauge-up"), (70, 100, "c-gauge-down")):
        parts.append(f'<path d="{_arc(cx, cy, r, start, end)}" class="{cls}" fill="none" '
                     f'stroke-width="13" stroke-linecap="round"/>')
    for tick in (0, 30, 50, 70, 100):
        tx, ty = _polar(cx, cy, r + 15, tick)
        parts.append(_text(tx, ty + 3.5, str(tick), anchor="middle", size=8.5))
    nx, ny = _polar(cx, cy, r - 20, value)
    parts.append(_line(cx, cy, nx, ny, cls="c-needle"))
    parts.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="3.2" class="c-dot"/>')
    parts.append(_text(cx, cy - 20, _num(value, 1), anchor="middle", size=25, weight=600))
    parts.append(_text(cx, cy + 16, label, anchor="middle", size=9.5, tone="--muted"))
    return _svg(width, height, "".join(parts), title,
                f"{title}: {value:.1f} of 100, {label}.")


def level_ladder(levels, last: float, *, width: int = 460, title: str = "Key levels") -> str:
    """A vertical price ladder: every level on one axis, nearest first by price."""
    rows = sorted(list(levels) + [(last, "Last close", "last")], key=lambda r: -r[0])
    row_h, header, footer = 25, 18, 8
    height = header + row_h * len(rows) + footer
    axis_left, axis_right = 132, 300
    values = [price for price, _, _ in rows]
    lo, hi = min(values), max(values)
    if hi == lo:
        hi = lo + 1
    def x(price):
        return axis_left + (hi - price) / (hi - lo) * (axis_right - axis_left)

    parts = [_text(0, 11, "Price", size=9, tone="--muted")]
    parts.append(_text(axis_right + 12, 11, "Distance from last", size=9, tone="--muted"))
    parts.append(_line(axis_left, header - 4, axis_left, height - footer, cls="c-grid"))
    for i, (price, name, kind) in enumerate(rows):
        cy = header + row_h * i + row_h / 2
        current = kind == "last"
        if current:
            parts.append(f'<rect x="0" y="{cy - row_h / 2 + 2:.1f}" width="{width}" '
                         f'height="{row_h - 4:.1f}" class="c-current-row" rx="4"/>')
        parts.append(_text(axis_left - 10, cy + 3.5, _num(price), anchor="end",
                           size=10, weight=600 if current else 400,
                           tone="--ink" if current else None))
        dot_cls = {"support": "c-dot-support", "resistance": "c-dot-resistance",
                   "last": "c-dot"}[kind]
        parts.append(f'<circle cx="{x(price):.1f}" cy="{cy:.1f}" r="{3.6 if current else 2.8}" '
                     f'class="{dot_cls}"/>')
        if current:
            parts.append(_text(axis_right + 12, cy + 3.5, "—", size=10, weight=600))
            continue
        parts.append(_text(axis_right + 12, cy + 3.5, name, size=9.5))
        parts.append(_text(width - 2, cy + 3.5, _distance(price, last), anchor="end", size=9.5,
                           tone="--up" if kind == "support" else "--down"))
    return _svg(width, height, "".join(parts), title,
                f"Key price levels around the last close of {last:.2f}.")


def _distance(price: float, reference: float) -> str:
    if not reference:
        return ""
    return _signed_pct((price - reference) / reference * 100)


def diverging_bars(items, *, width: int = 460, title: str = "Distance from benchmarks",
                   unit: str = "%") -> str:
    """Bars either side of zero, for readings such as price vs each average."""
    row_h, header, footer = 26, 18, 6
    height = header + row_h * len(items) + footer
    label_w, value_w = 132, 54
    plot_left, plot_right = label_w, width - value_w
    mid = (plot_left + plot_right) / 2
    half = (plot_right - plot_left) / 2 - 4
    extent = max(5.0, max(abs(v) for _, v in items))
    parts = [_text(0, 11, "Reference", size=9, tone="--muted"),
             _text(width - 2, 11, f"vs last ({unit})", anchor="end", size=9, tone="--muted")]
    parts.append(_line(mid, header - 4, mid, height - footer, cls="c-grid"))
    for i, (label, value) in enumerate(items):
        cy = header + row_h * i + row_h / 2
        parts.append(_text(0, cy + 3.5, label, size=10))
        length = abs(value) / extent * half
        x0 = mid - length if value < 0 else mid
        cls = "c-bar-down" if value < 0 else "c-bar-up"
        parts.append(f'<rect x="{x0:.1f}" y="{cy - 6:.1f}" width="{max(1.5, length):.1f}" '
                     f'height="12" rx="2" class="{cls}"/>')
        parts.append(_text(width - 2, cy + 3.5, _signed_pct(value, 2), anchor="end", size=10,
                           weight=600, tone="--down" if value < 0 else "--up"))
    return _svg(width, height, "".join(parts), title,
                "Each benchmark's distance from the last close.")


def prob_bars(items, *, width: int = 460, title: str = "Scenarios") -> str:
    """Horizontal probability bars: ``(label, percent, tone)``."""
    row_h, header, footer = 28, 18, 6
    height = header + row_h * len(items) + footer
    label_w, value_w = 150, 44
    bar_left, bar_right = label_w, width - value_w
    total = max(100.0, sum(max(0, p) for _, p, _ in items))
    parts = [_text(0, 11, "Scenario", size=9, tone="--muted"),
             _text(width - 2, 11, "Probability", anchor="end", size=9, tone="--muted")]
    for i, (label, pct, tone) in enumerate(items):
        cy = header + row_h * i + row_h / 2
        parts.append(_text(0, cy + 3.5, label, size=10))
        parts.append(f'<rect x="{bar_left}" y="{cy - 6:.1f}" width="{bar_right - bar_left}" '
                     f'height="12" rx="2" class="c-track"/>')
        w = max(1.5, (max(0, pct) / total) * (bar_right - bar_left))
        parts.append(f'<rect x="{bar_left}" y="{cy - 6:.1f}" width="{w:.1f}" '
                     f'height="12" rx="2" fill="var({tone})"/>')
        parts.append(_text(width - 2, cy + 3.5, f"{pct:g}%", anchor="end", size=10,
                           weight=600))
    return _svg(width, height, "".join(parts), title,
                "How the report's own scenarios split the odds.")


# --------------------------------------------------------------------------- #
# root
# --------------------------------------------------------------------------- #

def _svg(width: int, height: int, body: str, title: str, desc: str = "") -> str:
    label = escape(title, quote=True)
    description = f"<desc>{escape(desc)}</desc>" if desc else ""
    return (f'<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" '
            f'role="img" aria-label="{label}" class="chart-svg">'
            f"<title>{escape(title)}</title>{description}{body}</svg>")
