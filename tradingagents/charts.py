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
    "bar_chart",
    "line_chart",
    "range_bar",
    "trade_plan",
    "stacked_bar",
]


# --------------------------------------------------------------------------- #
# primitives
# --------------------------------------------------------------------------- #

_TRIM_CHARS = " （(【[·,/、;；:：-–— "


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


def _axis_gutter(labels, base: float = 42) -> float:
    """A left margin wide enough for the widest tick label at 8.5px.

    ``150,483.2`` is nine characters; the old fixed 42px margin clipped its
    leading digit against the viewBox edge.
    """
    widest = max((len(str(label)) for label in labels), default=0)
    return max(base, widest * 5.2 + 10)


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
    left, right = 52, 122
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
        cls = {"support": "c-level-support", "target": "c-level-support",
               "stop": "c-level-resistance"}.get(kind, "c-level")
        parts.append(_line(left, y(price), plot_right, y(price), cls=cls))
        label_items.append((y(price), f"{_num(price)}  {name}"))
    if not any(abs(price - close[-1]) < 0.005 for price, _name, _kind in levels):
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


def gauge(value: float, *, label: str = "", width: int = 280, height: int = 196,
          title: str = "Gauge") -> str:
    """A semicircular 0-100 gauge, for RSI or another bounded score."""
    value = max(0.0, min(100.0, float(value)))
    # The hub sits low; the reading goes *below* it so the needle never crosses
    # the number, and the tick labels keep clear of the arc and both edges.
    cx, cy = width / 2, height - 48
    r = min(width / 2 - 26, height - 80)
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
    parts.append(_text(cx, cy + 28, _num(value, 1), anchor="middle", size=22, weight=600))
    parts.append(_text(cx, cy + 42, label, anchor="middle", size=9.5, tone="--muted"))
    return _svg(width, height, "".join(parts), title,
                f"{title}: {value:.1f} of 100, {label}.")


def level_ladder(levels, last: float, *, width: int = 460, title: str = "Key levels") -> str:
    """A vertical price ladder: every level on one axis, nearest first by price."""
    items, has_last = [], False
    for price, name, kind in levels:
        if abs(float(price) - float(last)) < 0.005:
            items.append((price, name, "last"))
            has_last = True
        else:
            items.append((price, name, kind))
    if not has_last:
        items.append((last, "Last close", "last"))
    rows = sorted(items, key=lambda row: -row[0])
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
                   "last": "c-dot", "entry": "c-dot",
                   "stop": "c-dot-resistance", "target": "c-dot-support"}.get(kind, "c-dot")
        parts.append(f'<circle cx="{x(price):.1f}" cy="{cy:.1f}" r="{3.6 if current else 2.8}" '
                     f'class="{dot_cls}"/>')
        parts.append(_text(axis_right + 12, cy + 3.5, name, size=10 if current else 9.5,
                           weight=600 if current else 400))
        if current:
            parts.append(_text(width - 2, cy + 3.5, "\u2014", anchor="end", size=9.5,
                               weight=600))
            continue
        tone = {"support": "--up", "target": "--up",
                "resistance": "--down", "stop": "--down"}.get(kind, "--muted")
        parts.append(_text(width - 2, cy + 3.5, _distance(price, last), anchor="end", size=9.5,
                           tone=tone))
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


def _fit_label(text, max_px: float, size: float = 10) -> str:
    """Trim a label to the pixels available, counting CJK glyphs as a full em."""
    text = str(text)
    width = 0.0
    for index, char in enumerate(text):
        step = size if ord(char) > 0x2E80 else size * 0.55
        if width + step > max_px:
            head = text[:index].rstrip(_TRIM_CHARS)
            return (head or text[:index]) + "\u2026"
        width += step
    return text


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
        parts.append(_text(0, cy + 3.5, _fit_label(label, label_w - 8), size=10))
        parts.append(f'<rect x="{bar_left}" y="{cy - 6:.1f}" width="{bar_right - bar_left}" '
                     f'height="12" rx="2" class="c-track"/>')
        w = max(1.5, (max(0, pct) / total) * (bar_right - bar_left))
        parts.append(f'<rect x="{bar_left}" y="{cy - 6:.1f}" width="{w:.1f}" '
                     f'height="12" rx="2" fill="var({tone})"/>')
        parts.append(_text(width - 2, cy + 3.5, f"{pct:g}%", anchor="end", size=10,
                           weight=600))
    return _svg(width, height, "".join(parts), title,
                "How the report's own scenarios split the odds.")


def _clean(values):
    """The finite numbers in a series, for domain and extent work."""
    out = []
    for value in values or []:
        if value is None:
            continue
        try:
            number = float(value)
        except (TypeError, ValueError):
            continue
        if not math.isnan(number) and not math.isinf(number):
            out.append(number)
    return out


def _short(label: str, limit: int = 12) -> str:
    """Shorten a label without chopping a date or word mid-token."""
    text = str(label).strip()
    if len(text) <= limit:
        return text
    # A parenthetical tail is optional detail: drop it whole when it fits.
    for opener in ("（", "(", "【", "["):
        head = text.split(opener, 1)[0].strip()
        if 0 < len(head) <= limit:
            return head
    cut = text[:limit].rstrip(_TRIM_CHARS)
    if " " in cut:
        cut = cut.rsplit(" ", 1)[0]
    return (cut or text[: limit - 1]).rstrip(_TRIM_CHARS) + "\u2026"


def bar_chart(labels, values, *, width: int = 460, height: int = 190,
              title: str = "Bars", unit: str = "", tone: str = "--accent",
              tones=None, value_fmt=None, baseline_zero: bool = True) -> str:
    """Vertical bars for one series: revenue, EPS, margins, insider sales.

    ``tones`` can name a colour per bar (``"--up"`` / ``"--down"``); the default
    is ``tone``. Values are labelled above positive bars and below negative ones.
    """
    values = list(values or [])
    labels = list(labels or [])
    pairs = [(label, value) for label, value in zip(labels, values, strict=False)
             if value is not None and _clean([value])]
    if len(pairs) < 2:
        return ""
    labels = [str(label) for label, _ in pairs]
    values = [float(value) for _, value in pairs]
    fmt = value_fmt or (lambda value: _num(value))
    tones = list(tones or [])

    left, right, top, bottom = 42, 12, 18, 30
    plot_w = width - left - right
    plot_h = height - top - bottom
    lo, hi = min(values), max(values)
    if baseline_zero:
        lo, hi = min(0.0, lo), max(0.0, hi)
    if hi == lo:
        hi = lo + 1
    pad = (hi - lo) * 0.12
    if baseline_zero:
        lo = min(0.0, lo)
        if lo < 0:
            lo -= pad
        if hi > 0:
            hi += pad
    else:
        lo -= pad
        hi += pad

    ticks = _ticks(lo, hi, 4)
    left = _axis_gutter([_num(tick, 1) for tick in ticks], left)
    plot_w = width - left - right

    def y(value):
        return top + (hi - value) / (hi - lo) * plot_h

    parts = []
    for tick in ticks:
        parts.append(_line(left, y(tick), width - right, y(tick), cls="c-grid"))
        parts.append(_text(left - 7, y(tick) + 3.5, _num(tick, 1), anchor="end", size=8.5))
    if lo <= 0 <= hi:
        parts.append(_line(left, y(0), width - right, y(0), cls="c-level"))

    step = plot_w / len(values)
    bar_w = max(3.0, min(34.0, step * 0.62))
    base = 0.0 if baseline_zero else lo
    for i, (label, value) in enumerate(zip(labels, values, strict=False)):
        cx = left + step * (i + 0.5)
        x0 = cx - bar_w / 2
        y0, y1 = y(base), y(value)
        colour = tones[i] if i < len(tones) and tones[i] else (
            "--down" if value < 0 else ("--up" if baseline_zero else tone))
        parts.append(f'<rect x="{x0:.1f}" y="{min(y0, y1):.1f}" width="{bar_w:.1f}" '
                     f'height="{max(1.2, abs(y1 - y0)):.1f}" rx="2" fill="var({colour})" '
                     f'opacity="0.82"/>')
        label_y = min(y0, y1) - 5 if value >= 0 else max(y0, y1) + 11
        parts.append(_text(cx, label_y, fmt(value), anchor="middle", size=8.5,
                           weight=600, tone="--ink"))
        if len(labels) <= 8 or i % 2 == 0 or i == len(labels) - 1:
            parts.append(_text(cx, height - 9, _short(label), anchor="middle", size=8.5,
                               tone="--muted"))

    desc = f"{title}: {len(values)} bars" + (f", in {unit}." if unit else ".")
    return _svg(width, height, "".join(parts), title, desc)


def line_chart(labels, series, *, width: int = 460, height: int = 190,
               title: str = "Lines", unit: str = "", value_fmt=None) -> str:
    """One or more line series over the same labels, with a legend.

    ``series`` is ``[(name, values, tone, dash)]``; ``dash`` may be empty.
    """
    labels = list(labels or [])
    clean_series = []
    for name, values, tone, dash in series or []:
        points = _clean(values)
        if len(points) >= 2:
            clean_series.append((name, list(values), tone, dash or "1 0"))
    if len(labels) < 2 or not clean_series:
        return ""
    fmt = value_fmt or (lambda value: _num(value))
    all_values = [value for _name, values, _tone, _dash in clean_series for value in _clean(values)]
    lo, hi = min(all_values), max(all_values)
    if hi == lo:
        hi = lo + 1
    pad = (hi - lo) * 0.12
    lo -= pad
    hi += pad

    left, right, top, bottom = 42, 54, 26, 30
    ticks = _ticks(lo, hi, 4)
    left = _axis_gutter([_num(tick, 1) for tick in ticks], left)
    plot_w = width - left - right
    plot_h = height - top - bottom
    n = len(labels)

    def x(index):
        return left + index * plot_w / (n - 1)

    def y(value):
        return top + (hi - value) / (hi - lo) * plot_h

    parts = []
    for tick in ticks:
        parts.append(_line(left, y(tick), width - right, y(tick), cls="c-grid"))
        parts.append(_text(left - 7, y(tick) + 3.5, _num(tick, 1), anchor="end", size=8.5))
    for i in sorted({0, n // 4, n // 2, 3 * n // 4, n - 1}):
        parts.append(_text(x(i), height - 9, _short(labels[i]), anchor="middle", size=8.5,
                           tone="--muted"))

    cursor = left
    for name, values, tone, dash in clean_series:
        points = [(x(i), y(float(value))) for i, value in enumerate(values)
                  if value is not None and _clean([value])]
        parts.append(_polyline(points, cls="c-overlay", width=1.5,
                               extra=f' stroke="var({tone})" stroke-dasharray="{dash}"'))
        last = next((float(v) for v in reversed(values) if v is not None and _clean([v])), None)
        if last is not None:
            parts.append(f'<circle cx="{x(n - 1):.1f}" cy="{y(last):.1f}" r="2.2" '
                         f'fill="var({tone})"/>')
            parts.append(_text(width - 2, y(last) + 3.5, fmt(last), anchor="end", size=8.5,
                               weight=600, tone=tone))
        parts.append(_line(cursor, 10, cursor + 14, 10, cls="c-overlay",
                           extra=f' stroke="var({tone})" stroke-dasharray="{dash}"'))
        parts.append(_text(cursor + 18, 13, _short(name, 18), size=8.5, tone="--muted"))
        cursor += 24 + len(_short(name, 18)) * 4.6

    desc = f"{title}: {len(clean_series)} series" + (f", in {unit}." if unit else ".")
    return _svg(width, height, "".join(parts), title, desc)


def range_bar(low: float, high: float, current: float, *, markers=(),
              width: int = 460, height: int = 92, title: str = "Range",
              unit: str = "", value_fmt=None) -> str:
    """A horizontal range with the current value and optional markers."""
    low, high, current = float(low), float(high), float(current)
    if not (high > low):
        return ""
    current = max(low, min(high, current))
    fmt = value_fmt or (lambda value: _num(value))
    left, right, top, bottom = 18, 18, 34, 30
    plot_w = width - left - right
    axis_y = height - bottom

    def x(value):
        return left + (float(value) - low) / (high - low) * plot_w

    parts = [_line(left, axis_y, width - right, axis_y, cls="c-level")]
    parts.append(f'<circle cx="{x(current):.1f}" cy="{axis_y}" r="4" class="c-dot"/>')
    parts.append(_text(x(current), axis_y - 10, fmt(current), anchor="middle", size=9,
                       weight=600, tone="--ink"))
    parts.append(_text(left, axis_y + 15, fmt(low), size=8.5, tone="--muted"))
    parts.append(_text(width - right, axis_y + 15, fmt(high), anchor="end", size=8.5,
                       tone="--muted"))
    for value, label, tone in markers or []:
        if value is None or not (low <= float(value) <= high):
            continue
        mx = x(value)
        parts.append(_line(mx, axis_y - 7, mx, axis_y + 7, cls="c-level",
                           extra=f' stroke="var({tone or "--muted"})"'))
        parts.append(_text(mx, top - 6, _short(label, 14), anchor="middle", size=8.5,
                           tone=tone or "--muted"))
    desc = f"{title}: {fmt(low)} to {fmt(high)}, current {fmt(current)}"
    if unit:
        desc += f" ({unit})"
    return _svg(width, height, "".join(parts), title, desc + ".")


def trade_plan(entry: float, stop: float, targets=(), *, last: float | None = None,
               width: int = 640, height: int = 132, title: str = "Trade plan") -> str:
    """Entry, stop and targets on one price axis, with risk and reward shaded."""
    entry, stop = float(entry), float(stop)
    targets = [float(value) for value in targets or [] if value is not None]
    values = [entry, stop, *targets]
    if last is not None:
        values.append(float(last))
    if len(values) < 2 or max(values) == min(values):
        return ""
    low, high = min(values), max(values)
    pad = (high - low) * 0.08
    low, high = low - pad, high + pad
    left, right, top, bottom = 20, 20, 34, 30
    plot_w = width - left - right
    axis_y = height - bottom

    def x(value):
        return left + (float(value) - low) / (high - low) * plot_w

    parts = [_line(left, axis_y, width - right, axis_y, cls="c-level")]
    # Risk is the distance from entry down to the stop; reward is entry to the
    # furthest target. Washes sit under the axis so the labels stay readable.
    risk_x0, risk_x1 = sorted((x(entry), x(stop)))
    parts.append(f'<rect x="{risk_x0:.1f}" y="{top - 4:.1f}" width="{risk_x1 - risk_x0:.1f}" '
                 f'height="{axis_y - top + 4:.1f}" class="c-zone-down"/>')
    if targets:
        reward_x0, reward_x1 = sorted((x(entry), x(max(targets))))
        parts.append(f'<rect x="{reward_x0:.1f}" y="{top - 4:.1f}" '
                     f'width="{reward_x1 - reward_x0:.1f}" height="{axis_y - top + 4:.1f}" '
                     f'class="c-zone-up"/>')
    markers = [(stop, "Stop", "--down"), (entry, "Entry", "--ink")]
    markers += [(value, f"Target {i}", "--up") for i, value in enumerate(targets, 1)]
    if last is not None and all(abs(float(last) - value) > 0.005
                                for value, _label, _tone in markers):
        markers.append((float(last), "Last", "--muted"))
    for index, (value, label, tone) in enumerate(markers):
        mx = x(value)
        above = index % 2 == 0
        label_y = top - 8 if above else axis_y + 18
        parts.append(_line(mx, axis_y - 9, mx, axis_y + 9, cls="c-level",
                           extra=f' stroke="var({tone})" stroke-width="1.4"'))
        parts.append(f'<circle cx="{mx:.1f}" cy="{axis_y}" r="3" fill="var({tone})"/>')
        parts.append(_text(mx, label_y, f"{label} {_num(value)}", anchor="middle", size=8.5,
                           weight=600, tone=tone,
                           extra=' paint-order="stroke" stroke="var(--paper)" stroke-width="3"'))
    desc = f"Entry {_num(entry)}, stop {_num(stop)}"
    if targets:
        desc += ", targets " + ", ".join(_num(value) for value in targets)
    return _svg(width, height, "".join(parts), title, desc + ".")


def stacked_bar(items, *, width: int = 460, height: int = 78,
                title: str = "Composition") -> str:
    """One horizontal bar split into parts: ``(label, value, tone)``."""
    items = [(str(label), float(value), tone) for label, value, tone in items or []
             if value is not None and float(value) > 0]
    total = sum(value for _label, value, _tone in items)
    if total <= 0:
        return ""
    left, right, top = 14, 14, 22
    bar_h = 20
    plot_w = width - left - right
    parts = []
    cursor = left
    for _label, value, tone in items:
        segment = plot_w * value / total
        parts.append(f'<rect x="{cursor:.1f}" y="{top}" width="{max(1.0, segment):.1f}" '
                     f'height="{bar_h}" fill="var({tone})" opacity="0.82"/>')
        if segment > 34:
            parts.append(_text(cursor + segment / 2, top + 14, f"{value / total * 100:.0f}%",
                               anchor="middle", size=8.5, weight=600, tone="--paper"))
        cursor += segment
    cursor = left
    for label, _value, tone in items:
        parts.append(f'<circle cx="{cursor + 3}" cy="{top + bar_h + 17}" r="3" fill="var({tone})"/>')
        parts.append(_text(cursor + 10, top + bar_h + 20, _short(label, 16), size=8.5,
                           tone="--muted"))
        cursor += 26 + len(_short(label, 16)) * 4.6
    return _svg(width, height, "".join(parts), title,
                "A single bar split by " + ", ".join(label for label, _v, _t in items) + ".")


# --------------------------------------------------------------------------- #
# root
# --------------------------------------------------------------------------- #

def _svg(width: int, height: int, body: str, title: str, desc: str = "") -> str:
    label = escape(title, quote=True)
    description = f"<desc>{escape(desc)}</desc>" if desc else ""
    return (f'<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" '
            f'role="img" aria-label="{label}" class="chart-svg">'
            f"<title>{escape(title)}</title>{description}{body}</svg>")
