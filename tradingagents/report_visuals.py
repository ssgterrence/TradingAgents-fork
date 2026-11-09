"""Visual summaries for the self-contained HTML report.

The report's agents write prose. This module reads the same text the page
already renders, pulls out the numbers and tables that are unambiguous, and
turns them into cards and inline SVG charts. It never invents a value: when a
number or table cannot be read confidently the chart is omitted and the
original prose stays available in the page.

Nothing here calls an LLM. Every block is derived from the run's own text and
from ``chart_data`` (which reads the vendor OHLCV frame).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from html import escape

from markdown_it import MarkdownIt

from tradingagents import charts

# --------------------------------------------------------------------------- #
# text and table parsing
# --------------------------------------------------------------------------- #


@dataclass
class Table:
    """One GFM table, as plain text cells."""

    header: list[str] = field(default_factory=list)
    rows: list[list[str]] = field(default_factory=list)

    def column(self, *keywords: str) -> int | None:
        """The index of the first header cell containing every keyword."""
        for index, cell in enumerate(self.header):
            text = cell.lower()
            if all(keyword.lower() in text for keyword in keywords):
                return index
        return None

    def cell(self, row: list[str], index: int | None) -> str:
        if index is None or index >= len(row):
            return ""
        return row[index]


def _inline_plain(text: str) -> str:
    """Markdown inline text reduced to what a reader sees, with no tags."""
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", str(text))
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"(\*\*|__)(.*?)\1", r"\2", text)
    # Only paired emphasis markers, not the underscores in ``close_10_ema``.
    text = re.sub(r"(?<!\w)\*([^*]+)\*(?!\w)", r"\1", text)
    text = re.sub(r"(?<!\w)_([^_]+)_(?!\w)", r"\1", text)
    text = re.sub(r"~~(.*?)~~", r"\1", text)
    text = re.sub(r"<[^>]+>", "", text)
    return " ".join(text.split()).strip()


def tables(text: str) -> list[Table]:
    """Every GFM table in ``text``, parsed without rendering the prose."""
    if not text or "|" not in text:
        return []
    md = MarkdownIt("commonmark").enable("table")
    tokens = md.parse(text)
    found: list[Table] = []
    current: Table | None = None
    row: list[str] | None = None
    cell: list[str] | None = None
    in_header = False
    for token in tokens:
        if token.type == "table_open":
            current = Table()
        elif token.type == "thead_open":
            in_header = True
        elif token.type == "thead_close":
            in_header = False
        elif token.type == "tr_open":
            row = []
        elif token.type == "tr_close":
            if current is not None and row is not None:
                if in_header:
                    current.header = row
                else:
                    current.rows.append(row)
            row = None
        elif token.type in ("th_open", "td_open"):
            cell = []
        elif token.type == "inline" and cell is not None:
            cell.append(_inline_plain(token.content))
        elif token.type in ("th_close", "td_close"):
            if row is not None:
                row.append(" ".join(part for part in (cell or []) if part).strip())
            cell = None
        elif token.type == "table_close":
            if current is not None and (current.header or current.rows):
                found.append(current)
            current = None
    return found


_NUMBER_RE = re.compile(r"[-+]?\s*\$?\s*\d[\d,]*(?:\.\d+)?")


def _parse_number(raw: str) -> float | None:
    try:
        return float(raw.replace("$", "").replace(",", "").replace(" ", ""))
    except ValueError:
        return None


def number(text) -> float | None:
    """The first number in a cell, tolerating ``$``, ``,``, ``−`` and ``%``."""
    if text is None:
        return None
    raw = str(text).strip().replace("\u2212", "-").replace("\u2013", "-")
    if not raw or raw.lower() in {"none", "n/a", "na", "not provided", "—", "-", "–"}:
        return None
    match = _NUMBER_RE.search(raw)
    return _parse_number(match.group(0)) if match else None


def last_number(text) -> float | None:
    """The last number in a cell, for ``$3.17 / 59.3x`` style values."""
    if text is None:
        return None
    raw = str(text).strip().replace("\u2212", "-").replace("\u2013", "-")
    matches = _NUMBER_RE.findall(raw)
    return _parse_number(matches[-1]) if matches else None


def _table_matching(text: str, *groups, reject=None) -> Table | None:
    """The first table whose header has one alias from every group.

    A group is a tuple of alternatives, e.g. ``("revenue", "营收")``, so the
    same extractor works for English and Chinese reports. ``reject`` is an
    optional predicate that skips tables another extractor already owns.
    """
    for table in tables(text):
        if reject is not None and reject(table):
            continue
        header = " ".join(table.header).lower()
        if all(any(alias.lower() in header for alias in group) for group in groups):
            return table
    return None


def _column(table: Table, *names: str) -> int | None:
    for name in names:
        index = table.column(name)
        if index is not None:
            return index
    return None


def _signal(text: str) -> str:
    """Map a phrase to one of the four scorecard tones."""
    low = str(text).lower()
    if any(word in low for word in ("watch", "risk", "elevated", "expensive",
                                    "overhang", "compression", "mixed", "marginal",
                                    "关注", "风险", "高估", "分歧", "混合", "承压",
                                    "中性", "超卖", "极端延伸")):
        return "watch"
    # Chinese tables often use a bare 空 / 多 for the direction.
    tokens = set(re.split(r"[^0-9a-z\u4e00-\u9fff]+", low))
    if "空" in tokens or "偏空" in low:
        return "down"
    if "多" in tokens or "偏多" in low:
        return "up"
    if any(word in low for word in ("bearish", "negative", "below", "down",
                                    "rolling over", "falling", "deteriorat",
                                    "weak", "soft", "看空", "负面", "下行", "恶化",
                                    "走弱", "低于", "看跌", "谨慎", "利空")):
        return "down"
    if any(word in low for word in ("bullish", "positive", "above", "up",
                                    "improving", "reclaimed", "strong", "excellent",
                                    "constructive", "growth", "看多", "正面", "上行",
                                    "改善", "强劲", "增长", "高于", "看涨", "积极",
                                    "超预期", "利好")):
        return "up"
    return "neutral"


_INDICATOR_NAMES = {
    "close_10_ema": "10 EMA", "close_50_sma": "50 SMA", "close_200_sma": "200 SMA",
    "macd": "MACD", "macdh": "MACD hist", "macds": "MACD signal",
    "rsi": "RSI", "atr": "ATR", "vwma": "VWMA",
    "boll": "Bollinger mid", "boll_ub": "Bollinger upper", "boll_lb": "Bollinger lower",
}


def _indicator_label(text: str) -> str:
    clean = _inline_plain(text).strip().lower()
    return _INDICATOR_NAMES.get(clean, clean.replace("_", " "))


def _fmt(value: float, digits: int = 2) -> str:
    return f"{value:,.{digits}f}".replace("-", "\u2212")


def _pct(value: float, digits: int = 1, signed: bool = False) -> str:
    sign = ("+" if value > 0 else ("\u2212" if value < 0 else "")) if signed else (
        "\u2212" if value < 0 else "")
    return f"{sign}{abs(value):,.{digits}f}%"


# --------------------------------------------------------------------------- #
# extraction
# --------------------------------------------------------------------------- #


_LEVEL_RE = re.compile(
    r"\*\*([0-9][0-9,]*(?:\.[0-9]+)?)"
    r"(?:\s*[\u2013-]\s*[0-9][0-9,]*(?:\.[0-9]+)?)?\*\*"
    r"\s*[\u2014\u2013:-]\s*(.+)"
)


def _level_label(text: str) -> str:
    """A level's short name: the first clause, without a parenthetical aside."""
    clean = _inline_plain(text)
    clean = re.split(r"\s*[+;]\s*", clean)[0]
    clean = clean.split("(")[0]
    if ": " in clean:
        clean = clean.split(": ", 1)[1]
    clean = re.sub(r"\s+", " ", clean).strip(" :—-")
    return clean[:18]


_FIELD_RE = re.compile(r"\*\*([A-Za-z][A-Za-z ]{1,30})\*\*\s*:\s*([^\n]+)", re.IGNORECASE)


def extract_levels(texts) -> list[dict]:
    """Support, resistance and trade levels named in the report's own words."""
    text = "\n".join(str(part or "") for part in texts)
    levels: list[dict] = []
    kind = None
    for line in text.splitlines():
        low = line.lower()
        if "resistance ladder" in low or low.startswith("**resistance"):
            kind = "resistance"
        elif "support ladder" in low or low.startswith("**support"):
            kind = "support"
        match = _LEVEL_RE.search(line)
        if match and kind:
            price = number(match.group(1))
            label = _level_label(match.group(2))
            if price and 0 < price < 1_000_000:
                levels.append({"price": round(price, 2), "label": label, "kind": kind})

    # A report may present levels as a table instead of a ladder.
    for table in tables(text):
        price_col = _column(table, "price", "价位", "价格")
        label_col = _column(table, "level", "label", "name", "依据", "名称")
        kind_col = _column(table, "kind", "type", "类型")
        if price_col is None or label_col is None or price_col == label_col:
            # "Price vs. level" is a distance table, not a ladder.
            continue
        for row in table.rows:
            price = number(table.cell(row, price_col))
            if not price:
                continue
            row_kind = _inline_plain(table.cell(row, kind_col)).lower() if kind_col is not None else ""
            if "resist" in row_kind or "压力" in row_kind or "阻力" in row_kind:
                row_kind = "resistance"
            elif "support" in row_kind or "支撑" in row_kind:
                row_kind = "support"
            elif "目标" in row_kind:
                row_kind = "target"
            elif "触发" in row_kind or "止损" in row_kind:
                row_kind = "stop"
            elif "枢轴" in row_kind or "裁判" in row_kind or "首关" in row_kind:
                row_kind = "resistance"
            else:
                row_kind = "resistance" if price > 0 else "support"
            levels.append({"price": round(price, 2),
                           "label": _level_label(table.cell(row, label_col)),
                           "kind": row_kind})

    # The trader's own plan is the most actionable set of levels.
    for field_name, kind_name in (("Entry Price", "entry"), ("Stop Loss", "stop"),
                             ("Price Target", "target"), ("Target", "target")):
        match = re.search(rf"\*\*{field_name}\*\*\s*:\s*([^\n]+)", text, re.IGNORECASE)
        if not match:
            continue
        price = number(match.group(1))
        if price and 0 < price < 1_000_000:
            levels.append({"price": round(price, 2), "label": field_name,
                           "kind": kind_name})

    seen, unique = set(), []
    for level in levels:
        key = (round(level["price"], 2), level["label"].lower())
        if key not in seen:
            seen.add(key)
            unique.append(level)
    return unique[:12]


_SCENARIO_LABEL_RE = re.compile(
    r"(?i)(base case|bull case|bear case|base|bullish|bearish|bull|bear|"
    r"情景\s*[A-Za-z一二三四五]|基准|牛市|熊市)"
)


def extract_scenarios(text: str) -> list[dict]:
    """The report's own odds, when it states them as percentages.

    The percentage is read from the 200 characters after the label, so both
    ``~55% weight`` and ``概率 55%`` work without a second pattern per language.
    """
    found: list[dict] = []
    seen = set()
    text = text or ""
    for match in _SCENARIO_LABEL_RE.finditer(text):
        label = match.group(1).title()
        if label.lower() in seen:
            continue
        tail = text[match.end():match.end() + 200]
        percent = re.search(r"(\d{1,3})\s*%", tail)
        if not percent:
            continue
        probability = int(percent.group(1))
        if not 0 <= probability <= 100:
            continue
        seen.add(label.lower())
        low = label.lower()
        tone = "--down" if ("bear" in low or "熊" in low) else (
            "--up" if ("bull" in low or "牛" in low) else "--ink")
        found.append({"label": label, "prob": probability, "tone": tone})
    return found[:5]


def extract_trade_plan(final_state: dict) -> dict:
    """The trader's and PM's concrete fields, read from their rendered markdown."""
    text = "\n".join(str(final_state.get(key) or "") for key in
                     ("trader_investment_plan", "final_trade_decision"))
    plan: dict = {}
    for match in _FIELD_RE.finditer(text):
        key = match.group(1).strip().lower().replace(" ", "_")
        if key in {"action", "rating", "entry_price", "stop_loss", "price_target",
                   "position_sizing", "time_horizon"}:
            plan.setdefault(key, match.group(2).strip())
    for key in ("entry_price", "stop_loss", "price_target"):
        plan[key + "_num"] = number(plan.get(key))
    action = _inline_plain(plan.get("action", ""))
    plan["action"] = action.split()[0] if action else ""
    plan["rating"] = _inline_plain(plan.get("rating", ""))
    return plan


_SENTIMENT_RE = re.compile(
    r"\*\*Overall Sentiment:\*\*\s*\*\*(.+?)\*\*\s*\(Score:\s*([\d.]+)/10\)",
    re.IGNORECASE,
)


def extract_sentiment(text: str) -> dict | None:
    match = _SENTIMENT_RE.search(text or "")
    if not match:
        return None
    confidence = re.search(r"\*\*Confidence:\*\*\s*(\w+)", text, re.IGNORECASE)
    return {"band": match.group(1), "score": float(match.group(2)),
            "confidence": confidence.group(1) if confidence else ""}


def extract_macro_kpis(text: str) -> list[dict]:
    """The macro strip: rates, Fed, inflation, labour, growth, volatility."""
    table = _table_matching(text, ("category", "类别"), ("data point", "指标", "事件", "detail"))
    if table is None:
        table = _table_matching(text, ("category", "类别"), ("value", "数值", "最新值"))
    kpis: list[dict] = []
    if table is not None:
        category = _column(table, "category", "类别")
        point = _column(table, "data point", "指标", "事件", "detail")
        value = _column(table, "value", "最新值", "数值", "data")
        read = _column(table, "read", "含义", "解读")
        seen = set()
        for row in table.rows:
            cat = _inline_plain(table.cell(row, category)).lower()
            name = _inline_plain(table.cell(row, point)) if point is not None else ""
            raw = _inline_plain(table.cell(row, value)) if value is not None else ""
            if not raw:
                continue
            key = f"{cat} {name}".lower()
            label = None
            if "prediction" in cat or "预测" in cat:
                continue
            if "10y ust" in key or ("rates" in cat and "10y" in key) or ("美债" in key and "10y" in key):
                label = "10Y UST"
            elif "10y" in key and "2y" in key:
                label = "10Y–2Y"
            elif "effective ffr" in key or "fed funds" in key or "联邦基金" in key or "有效联邦" in key:
                label = "Fed funds"
            elif "core pce" in key or "核心pce" in key or "核心 pce" in key:
                label = "Core PCE"
            elif "cpi" in key:
                label = "CPI"
            elif "unemployment" in key or "失业" in key:
                label = "Unemployment"
            elif "gdp" in key:
                label = "Real GDP"
            elif "vix" in key:
                label = "VIX"
            if label and label not in seen:
                seen.add(label)
                note = _inline_plain(table.cell(row, read)) if read is not None else cat.title()
                kpis.append({"label": label, "value": raw[:54],
                             "note": note[:48], "tone": _signal(raw)})
    if kpis:
        return kpis[:8]

    patterns = (
        ("10Y UST", r"10Y UST[:\s]+([\d.]+%)"),
        ("Fed funds", r"Effective fed funds[:\s]+([\d.]+%)"),
        ("CPI", r"CPI[:\s]+([\d.]+)"),
        ("VIX", r"VIX[:\s]+([\d.]+)"),
        ("Unemployment", r"Unemployment[:\s]+([\d.]+%)"),
        ("Real GDP", r"Real GDP[:\s]+([^\n;]+)"),
    )
    for label, pattern in patterns:
        match = re.search(pattern, text or "", re.IGNORECASE)
        if match:
            kpis.append({"label": label, "value": match.group(1).strip()[:42],
                         "note": "", "tone": "neutral"})
    return kpis[:8]


def extract_prediction_markets(text: str) -> list[dict]:
    table = _table_matching(text, ("market", "市场"), ("implied", "概率", "prob"))
    rows = []
    if table is not None:
        market = _column(table, "market", "市场")
        probability = _column(table, "implied", "概率", "prob")
        volume = _column(table, "volume", "成交量", "金额")
        for row in table.rows:
            label = _inline_plain(table.cell(row, market))
            prob = number(table.cell(row, probability))
            if not label or prob is None:
                continue
            low = label.lower()
            tone = "--down" if any(word in low for word in
                                   ("recession", "bubble", "shutdown", "衰退", "泡沫", "降息")) \
                else "--accent"
            rows.append({"label": label[:46], "prob": prob,
                         "volume": _inline_plain(table.cell(row, volume)), "tone": tone})
    if rows:
        return rows[:6]

    # Chinese reports often state the odds as quoted bullets instead of a table.
    for match in re.finditer(
            r"[\u201c\"]([^\u201d\"]{3,80})[\u201d\"]\s*[:\uff1a]?\s*(?:Yes\s*)?(\d{1,3})\s*%",
            text or "", re.IGNORECASE):
        label = _inline_plain(match.group(1))
        prob = int(match.group(2))
        if not 0 <= prob <= 100:
            continue
        low = label.lower()
        tone = "--down" if any(word in low for word in
                               ("衰退", "泡沫", "降息", "recession", "bubble")) else "--accent"
        rows.append({"label": label[:46], "prob": prob, "volume": "", "tone": tone})
    return rows[:6]


def extract_peer_results(text: str) -> list[dict]:
    table = _table_matching(text, ("peer", "同行", "公司"), ("result", "结果"))
    if table is None:
        return []
    peer = _column(table, "peer", "同行", "公司")
    result = _column(table, "result", "结果")
    implication = _column(table, "implication", "含义", "解读")
    rows = []
    for row in table.rows:
        name = _inline_plain(table.cell(row, peer))
        outcome = _inline_plain(table.cell(row, result))
        if not name:
            continue
        low = outcome.lower()
        tone = "up" if "beat" in low else ("down" if "miss" in low else "neutral")
        rows.append({"peer": name, "result": outcome,
                     "implication": _inline_plain(table.cell(row, implication)),
                     "tone": tone})
    return rows[:8]


def extract_news_flow(text: str) -> tuple[int, int]:
    """Approximate the constructive/cautious split of the news bullets."""
    def count(start: str, stop: str) -> int:
        match = re.search(rf"{re.escape(start)}(.*?)(?={re.escape(stop)}|\Z)",
                          text or "", re.IGNORECASE | re.DOTALL)
        if not match:
            return 0
        return len(re.findall(r"^\s*[-*]\s+\*\*", match.group(1), re.MULTILINE))

    positive = count("Constructive / thesis-reinforcing", "Cautious / overhang")
    cautious = count("Cautious / overhang", "Notable")
    return positive, cautious


def extract_catalysts(text: str) -> list[dict]:
    """The dated lines from the calendar section, in reading order."""
    match = re.search(r"##[^\n]*(?:Calendar|日历|催化剂|关注)[^\n]*\n(.*?)(?=\n##|\Z)",
                      text or "", re.IGNORECASE | re.DOTALL)
    section = match.group(1) if match else ""
    items = []
    for line in section.splitlines():
        clean = _inline_plain(line)
        if not clean or not line.strip().startswith(("-", "*")):
            continue
        date = re.search(r"(20\d{2}-\d{2}-\d{2}|late \w+|early \w+|next \w+|FOMC)", clean,
                         re.IGNORECASE)
        when = date.group(1) if date else "Watch"
        what = clean
        if date:
            what = clean[: date.start()] + clean[date.end():]
        what = what.strip(" ~:—-/")
        if what:
            items.append({"when": when, "what": what[:110]})
    return items[:6]


def _first_sentence(text: str, limit: int = 220) -> str:
    clean = _inline_plain(text)
    if not clean:
        return ""
    sentence = re.split(r"(?<=[.!?。！？])\s+", clean)[0]
    return sentence[:limit].rstrip() + ("…" if len(sentence) > limit else "")


def extract_arguments(text: str, limit: int = 6) -> list[dict]:
    """Heading + first sentence pairs from a debate side."""
    if not text:
        return []
    parts = re.split(r"^##\s+", text, flags=re.MULTILINE)
    found, seen = [], set()
    for part in parts[1:]:
        lines = [line for line in part.splitlines() if line.strip()]
        if not lines:
            continue
        heading = _inline_plain(lines[0]).strip("# ").strip()
        body = "\n".join(lines[1:])
        summary = _first_sentence(body)
        key = heading.lower()[:40]
        if key and key not in seen:
            seen.add(key)
            found.append({"title": heading[:90], "summary": summary})
        if len(found) >= limit:
            break
    if found:
        return found
    paragraphs = [p for p in re.split(r"\n\s*\n", text) if _inline_plain(p)]
    return [{"title": f"Point {i}", "summary": _first_sentence(p)}
            for i, p in enumerate(paragraphs[:limit], 1)]


# --------------------------------------------------------------------------- #
# HTML blocks
# --------------------------------------------------------------------------- #


def figure(svg: str, caption: str, *, wide: bool = False) -> str:
    if not svg:
        return ""
    hint = (' <span class="scroll-hint">Scroll sideways to see the whole window.</span>'
            if wide else "")
    return (f'<figure class="chart{" wide" if wide else ""}">'
            f'<div class="plot">{svg}</div>'
            f"<figcaption>{caption}{hint}</figcaption></figure>")


def kpis(items) -> str:
    cards = []
    for item in items or []:
        value = item.get("value")
        if value in (None, ""):
            continue
        tone = escape(str(item.get("tone", "")))
        extra = " text" if len(str(value)) > 16 else ""
        classes = f"kpi {tone}{extra}".strip()
        cards.append(
            f'<div class="{classes}">'
            f'<div class="label">{escape(str(item.get("label", "")))}</div>'
            f'<div class="value">{escape(str(value))}</div>'
            f'<div class="note">{escape(str(item.get("note", "")))}</div></div>'
        )
    return f'<div class="kpis">{"".join(cards)}</div>' if cards else ""


def scorecard(rows) -> str:
    if not rows:
        return ""
    chinese = any(re.search(r"[\u4e00-\u9fff]", str(cell)) for row in rows for cell in row)
    headings = (("指标", "数值", "信号", "说明") if chinese
                else ("Metric", "Value", "Signal", "Why it matters"))
    body = []
    for row in rows:
        label, value, signal, note = row
        tone = signal if signal in {"up", "down", "watch", "neutral"} else _signal(signal)
        body.append(
            '<div class="score-row">'
            f'<span class="score-label">{escape(str(label))}</span>'
            f'<span class="score-value">{escape(str(value))}</span>'
            f'<span class="score-signal {tone}">{escape(str(signal))}</span>'
            f'<span class="score-note">{escape(str(note))}</span>'
            "</div>"
        )
    head = "".join(f"<span>{escape(text)}</span>" for text in headings)
    return ('<div class="scorecard"><div class="score-head">'
            + head + "</div>" + "".join(body) + "</div>")


def card(title: str, body: str, *, tone: str = "", meta: str = "") -> str:
    meta_html = f'<div class="vcard-meta">{escape(meta)}</div>' if meta else ""
    return (f'<article class="vcard {escape(tone)}">'
            f'<div class="vcard-title">{escape(title)}</div>'
            f"{meta_html}<div class=\"vcard-body\">{body}</div></article>")


def timeline(items) -> str:
    if not items:
        return ""
    rows = "".join(
        f'<li><span class="when">{escape(str(item["when"]))}</span>'
        f'<span class="what">{escape(str(item["what"]))}</span></li>'
        for item in items
    )
    return f'<ol class="timeline">{rows}</ol>'


def pills(items) -> str:
    if not items:
        return ""
    return '<div class="pills">' + "".join(
        f'<span class="pill {escape(tone)}">{escape(label)}</span>'
        for label, tone in items
    ) + "</div>"


def table_html(table: Table) -> str:
    head = "".join(f"<th>{escape(cell)}</th>" for cell in table.header)
    body = "".join(
        "<tr>" + "".join(f"<td>{escape(cell)}</td>" for cell in row) + "</tr>"
        for row in table.rows
    )
    return f'<div class="table"><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


def _grid(cards, columns: int = 2) -> str:
    if not cards:
        return ""
    return f'<div class="vgrid cols-{columns}">' + "".join(cards) + "</div>"


def _bullets(text: str, limit: int = 4) -> list[str]:
    """The bold lead-ins of a section, which are its own key points."""
    leads = []
    for match in re.finditer(r"^\s*[-*]\s+\*\*(.+?)\*\*", text or "", re.MULTILINE):
        lead = _inline_plain(match.group(1))
        if lead and lead not in leads:
            leads.append(lead[:120])
        if len(leads) >= limit:
            break
    return leads


# --------------------------------------------------------------------------- #
# section summaries
# --------------------------------------------------------------------------- #


def market_charts(chart_data: dict) -> str:
    """The indicator panels under the Market Analyst's heading."""
    rsi = chart_data.get("rsi") or {}
    macd = chart_data.get("macd") or {}
    distances = chart_data.get("distances") or []
    blocks = []
    rsi_svg = charts.rsi_panel(rsi.get("dates", []), rsi.get("values", []))
    if rsi_svg:
        blocks.append(figure(rsi_svg, "<b>Momentum is washed out, not yet improving.</b> "
                                      "The 30/70 lines are the oversold and overbought "
                                      "thresholds; the last print is labelled.", wide=True))
    macd_svg = charts.macd_panel(macd.get("dates", []), macd.get("macd", []),
                                 macd.get("signal", []), macd.get("histogram", []))
    if macd_svg:
        blocks.append(figure(macd_svg, "<b>The crossover is the pending trigger.</b> "
                                      "Bars are the histogram; the dashed line is the signal.",
                             wide=True))
    if distances:
        blocks.append(figure(
            charts.diverging_bars([(row["label"], row["value"]) for row in distances]),
            "<b>Price against every benchmark.</b> Bars left of zero are the distance "
            "from each average or band, in per cent.", wide=True))
    return "".join(blocks)


def market_summary(text: str, chart_data: dict) -> str:
    blocks = []

    # The report's own regime sentence, as three pills.
    low = (text or "").lower()
    regime = []
    for label, pattern in (("Long-term up", r"long-term[^.]{0,40}up"),
                           ("Medium-term down", r"medium-term[^.]{0,40}down"),
                           ("Short-term up", r"short-term[^.]{0,40}up")):
        if re.search(pattern, low):
            regime.append((label, "up" if "up" in label.lower() else "down"))
    if regime:
        blocks.append(pills(regime))

    # A Chinese report often closes with a dimension/reading/direction table.
    regime_table = _table_matching(text, ("维度", "dimension"), ("读数", "reading", "事实"))

    def _is_regime(table) -> bool:
        return _column(table, "维度", "dimension") is not None

    # The eight-indicator table is the best single view of the market section.
    # Reject the dimension table above so it is not scored twice with blank
    # value/why columns (its headers are "指标 / 数据", "读数", "信号方向").
    table = _table_matching(text, ("indicator", "指标"),
                            ("signal", "信号", "方向", "当前值", "为何"),
                            reject=_is_regime)
    if table is not None:
        name = _column(table, "indicator", "指标")
        value = _column(table, "value", "当前值", "数值", "读数", "data")
        signal = _column(table, "signal", "方向", "信号")
        why = _column(table, "why", "为何", "含义", "说明", "note")
        rows = []
        for row in table.rows:
            label = _indicator_label(table.cell(row, name))
            if not label:
                continue
            rows.append((label, _inline_plain(table.cell(row, value)),
                         _inline_plain(table.cell(row, signal)),
                         _inline_plain(table.cell(row, why))[:70]))
        if rows:
            blocks.append(scorecard(rows))

    # A Chinese report often closes with a dimension/reading/direction table.
    regime_table = _table_matching(text, ("维度", "dimension"), ("读数", "reading", "事实"))
    if regime_table is not None:
        label_col = _column(regime_table, "维度", "dimension")
        read_col = _column(regime_table, "读数", "reading", "事实")
        direction_col = _column(regime_table, "方向", "direction")
        weight_col = _column(regime_table, "权重", "weight")
        note_col = _column(regime_table, "说明", "note", "why")
        note_col = weight_col if weight_col is not None else note_col
        rows, trend_pills = [], []
        for row in regime_table.rows:
            label = _inline_plain(regime_table.cell(row, label_col))
            if not label:
                continue
            direction = _inline_plain(regime_table.cell(row, direction_col))
            rows.append((label, _inline_plain(regime_table.cell(row, read_col)),
                         direction, _inline_plain(regime_table.cell(row, note_col))[:70]))
            if any(word in label for word in ("长期", "中期", "短期", "long-term",
                                              "medium-term", "short-term")):
                trend_pills.append((f"{label} · {direction}", _signal(direction)))
        if rows:
            blocks.append(scorecard(rows))
        if trend_pills:
            blocks.append(pills(trend_pills[:3]))

    # The volume table makes the "down days heavier" point concrete.
    volume = _table_matching(text, ("session", "日期", "交易日"), ("volume", "成交量"))
    if volume is not None:
        session = _column(volume, "session", "日期", "交易日")
        change = _column(volume, "close change", "涨跌", "收盘")
        amount = _column(volume, "volume", "成交量")
        labels, values, tones = [], [], []
        for row in volume.rows:
            label = _inline_plain(volume.cell(row, session))
            size = number(volume.cell(row, amount))
            if not label or size is None:
                continue
            labels.append(label[-5:] if len(label) > 5 else label)
            values.append(size)
            change_text = volume.cell(row, change)
            tones.append("--down" if ("\u2212" in change_text or change_text.strip().startswith("-"))
                         else "--up")
        if len(labels) >= 2:
            blocks.append(figure(
                charts.bar_chart(labels, values, title="Volume by session",
                                 tones=tones, value_fmt=lambda value: f"{value:,.1f}M"),
                "<b>Down days are carrying heavier volume than up days.</b> "
                "Bars are coloured by the session's direction.", wide=True))

    return "".join(blocks)


def news_summary(text: str) -> str:
    blocks = []
    macro = extract_macro_kpis(text)
    if macro:
        blocks.append(kpis(macro))

    positive, cautious = extract_news_flow(text)
    if positive or cautious:
        blocks.append(figure(
            charts.stacked_bar([("Constructive", positive, "--up"),
                                ("Cautious", cautious, "--down")],
                               title="News flow"),
            "<b>The news flow is not one-sided.</b> The bar counts the constructive "
            "and cautious items the analyst listed."))

    markets = extract_prediction_markets(text)
    if markets:
        blocks.append(figure(
            charts.prob_bars([(row["label"], row["prob"], row["tone"]) for row in markets],
                             title="Prediction-market odds"),
            "<b>What the crowd is pricing.</b> Implied probabilities from the report's "
            "prediction-market table.", wide=True))

    peers = extract_peer_results(text)
    if peers:
        cards = []
        for row in peers:
            body = (f'<p>{escape(row["result"])}</p>'
                    f'<p class="muted">{escape(row["implication"])}</p>')
            cards.append(card(row["peer"], body, tone=row["tone"]))
        blocks.append(_grid(cards, 3))

    catalysts = extract_catalysts(text)
    if catalysts:
        blocks.append('<h4 class="vheading">What to watch next</h4>' + timeline(catalysts))

    return "".join(blocks)


def _table_numbers(table: Table, label_col: int, value_cols) -> tuple[list[str], list[list[float]]]:
    labels, series = [], [[] for _ in value_cols]
    for row in table.rows:
        label = _inline_plain(table.cell(row, label_col))
        if not label:
            continue
        values = [number(table.cell(row, col)) for col in value_cols]
        if all(value is None for value in values):
            continue
        labels.append(label[:14])
        for index, value in enumerate(values):
            series[index].append(value)
    return labels, series


def fundamentals_summary(text: str) -> str:
    blocks = []

    # Key-point cards are the report's own summary table.
    keypoints = _table_matching(text, ("category", "维度", "类别"),
                                ("detail", "关键数据", "事实"))
    if keypoints is not None:
        category = _column(keypoints, "category", "维度", "类别")
        detail = _column(keypoints, "detail", "关键数据", "事实")
        signal = _column(keypoints, "signal", "方向", "解读")
        wanted = ("ttm revenue", "latest quarter", "gross margin", "operating margin",
                  "net margin", "cash generation", "valuation", "insider",
                  "营收", "季度", "毛利率", "营业利润率", "净利率", "现金流",
                  "估值", "内部人")
        cards = []
        for row in keypoints.rows:
            name = _inline_plain(keypoints.cell(row, category))
            if not any(word in name.lower() for word in wanted):
                continue
            value = _inline_plain(keypoints.cell(row, detail))
            if not value:
                continue
            tone = _signal(_inline_plain(keypoints.cell(row, signal)))
            cards.append({"label": name[:24], "value": value[:60],
                          "note": _inline_plain(keypoints.cell(row, signal))[:40],
                          "tone": tone})
        if cards:
            blocks.append(kpis(cards[:8]))

    # Six-quarter growth: revenue, margins, EPS.
    quarterly = _table_matching(text, ("quarter", "季度"), ("revenue", "营收"))
    if quarterly is not None:
        label_col = _column(quarterly, "quarter", "季度")
        revenue_col = _column(quarterly, "revenue", "营收")
        gross_col = _column(quarterly, "gross %", "gross margin", "毛利率")
        op_col = _column(quarterly, "op %", "operating margin", "营业利润率")
        eps_col = _column(quarterly, "eps", "摊薄eps", "每股收益")
        if label_col is not None and revenue_col is not None:
            labels, series = _table_numbers(quarterly, label_col, [revenue_col])
            if labels:
                blocks.append(figure(
                    charts.bar_chart(labels, series[0], title="Quarterly revenue",
                                     value_fmt=lambda value: f"{value:,.0f}M"),
                    "<b>Revenue is accelerating.</b> Six quarters, in the report's own "
                    "units (millions).", wide=True))
        if label_col is not None and (gross_col is not None or op_col is not None):
            cols = [col for col in (gross_col, op_col) if col is not None]
            labels, series = _table_numbers(quarterly, label_col, cols)
            if labels:
                lines = []
                names = ["Gross margin", "Operating margin"]
                for index, values in enumerate(series):
                    lines.append((names[index], values, "--accent" if index == 0 else "--muted",
                                  "1 0" if index == 0 else "4 3"))
                blocks.append(figure(
                    charts.line_chart(labels, lines, title="Margins",
                                      value_fmt=lambda value: f"{value:.1f}%"),
                    "<b>Margins are the swing variable.</b> Gross and operating margin "
                    "across the same six quarters.", wide=True))
        if label_col is not None and eps_col is not None:
            labels, series = _table_numbers(quarterly, label_col, [eps_col])
            if labels:
                blocks.append(figure(
                    charts.bar_chart(labels, series[0], title="Quarterly EPS",
                                     value_fmt=lambda value: f"${value:,.2f}"),
                    "<b>EPS is compounding.</b> Diluted EPS per quarter, as reported."))

    # Annual history.
    annual = _table_matching(text, ("fy", "财年", "年度"), ("revenue", "营收"))
    if annual is not None:
        label_col = _column(annual, "fy", "财年", "年度")
        revenue_col = _column(annual, "revenue", "营收")
        eps_col = _column(annual, "diluted eps", "eps", "摊薄eps", "每股收益")
        if label_col is not None and revenue_col is not None:
            labels, series = _table_numbers(annual, label_col, [revenue_col])
            if labels:
                blocks.append(figure(
                    charts.bar_chart(labels, series[0], title="Annual revenue",
                                     value_fmt=lambda value: f"{value:,.0f}M"),
                    "<b>The long-run compounding record.</b> Revenue by fiscal year, "
                    "in the report's own units.", wide=True))
        if label_col is not None and eps_col is not None:
            labels, series = _table_numbers(annual, label_col, [eps_col])
            if labels:
                blocks.append(figure(
                    charts.line_chart(labels, [("Diluted EPS", series[0], "--accent", "1 0")],
                                      title="Annual EPS",
                                      value_fmt=lambda value: f"${value:,.2f}"),
                    "<b>Split-adjusted EPS.</b> The report marks the adjusted years."))

    # Cash-flow quality.
    cash = _table_matching(text, ("period", "期间", "项目"),
                           ("operating cf", "经营现金流", "经营现金流净额", "ocf"))
    if cash is not None:
        label_col = _column(cash, "period", "期间", "项目")
        ocf_col = _column(cash, "operating cf", "经营现金流", "经营现金流净额", "ocf")
        if label_col is not None and ocf_col is not None:
            labels, series = _table_numbers(cash, label_col, [ocf_col])
            if labels:
                blocks.append(figure(
                    charts.bar_chart(labels, series[0], title="Operating cash flow",
                                     value_fmt=lambda value: f"{value:,.0f}M"),
                    "<b>Cash generation is the quality check.</b> Operating cash flow "
                    "by period; the report's conversion ratio is in the table.", wide=True))

    # Balance sheet: assets, liabilities, equity.
    balance = _table_matching(text, ("item", "项目"), ("change", "变化", "2026-06-30"))
    if balance is None:
        for candidate in tables(text):
            joined = " ".join(" ".join(row) for row in candidate.rows)
            if "总资产" in joined or "Total assets" in joined:
                balance = candidate
                break
    if balance is not None:
        item_col = _column(balance, "item", "项目")
        value_col = _column(balance, "2026-06-30", "2026-09-30", "2026-03-31")
        if value_col is None:
            # The first value column after the item name.
            value_col = 1 if len(balance.header) > 1 else None
        labels, values = [], []
        for row in balance.rows:
            name = _inline_plain(balance.cell(row, item_col))
            if not name or not any(word in name.lower() for word in
                                   ("total assets", "total liabilities", "stockholders",
                                    "总资产", "总负债", "股东权益", "所有者权益")):
                continue
            value = number(balance.cell(row, value_col))
            if value is None:
                continue
            labels.append(name[:18])
            values.append(value)
        if len(values) >= 2:
            blocks.append(figure(
                charts.bar_chart(labels, values, title="Balance sheet",
                                 value_fmt=lambda value: f"${value:,.0f}M"),
                "<b>A debt-free balance sheet.</b> Assets, liabilities and equity at "
                "the latest reported date.", wide=True))

    # Valuation multiples.
    valuation = _table_matching(text, ("metric", "指标"), ("anet", "数值", "value"))
    if valuation is not None:
        metric_col = _column(valuation, "metric", "指标")
        value_col = _column(valuation, "anet", "数值", "value")
        wanted = ("ttm eps", "forward eps", "peg", "p/b", "p/s", "p/fcf",
                  "市盈率", "市销率", "市净率", "peg")
        labels, values, seen = [], [], set()
        for row in valuation.rows:
            name = _inline_plain(valuation.cell(row, metric_col))
            if not any(word in name.lower() for word in wanted):
                continue
            value = last_number(valuation.cell(row, value_col))
            if value is None:
                continue
            label = name.split("/")[0].strip()[:12]
            if label.lower() in seen:
                continue
            seen.add(label.lower())
            labels.append(label)
            values.append(value)
        if len(values) >= 2:
            blocks.append(figure(
                charts.bar_chart(labels, values, title="Valuation multiples",
                                 baseline_zero=False,
                                 value_fmt=lambda value: f"{value:,.1f}x"),
                "<b>Priced for growth.</b> The report's own multiples; bars are not "
                "comparable units, so read them as a level check.", wide=True))

    # Insider selling.
    insider = _table_matching(text, ("insider", "内部人"),
                              ("recent sales", "卖出", "value"))
    if insider is not None:
        name_col = _column(insider, "insider", "内部人")
        value_col = _column(insider, "value", "approx", "金额")
        labels, values = [], []
        for row in insider.rows:
            name = _inline_plain(insider.cell(row, name_col))
            value = number(insider.cell(row, value_col))
            if not name or value is None:
                continue
            labels.append(name.split()[0][:12])
            values.append(value)
        if values:
            blocks.append(figure(
                charts.bar_chart(labels, values, title="Insider selling",
                                 tones=["--down"] * len(values),
                                 value_fmt=lambda value: f"${value:,.0f}M"),
                "<b>One-sided insider supply.</b> Approximate value sold in the "
                "report's window; the table notes there were no open-market purchases."))

    return "".join(blocks)


def sentiment_summary(text: str) -> str:
    parsed = extract_sentiment(text)
    if not parsed:
        return ""
    blocks = [figure(
        charts.gauge(parsed["score"] * 10,
                     label=f"{parsed['band']} · {parsed['score']:.1f}/10"),
        f"<b>Community sentiment: {escape(parsed['band'])}.</b> "
        f"Confidence {escape(parsed['confidence'] or 'not stated')}; the gauge maps "
        "the report's 0–10 score onto the same 0–100 scale as RSI.")]
    table = _table_matching(text, ("signal", "情绪信号"), ("direction", "方向"))
    if table is not None:
        signal_col = _column(table, "signal", "情绪信号")
        direction = _column(table, "direction", "方向")
        evidence = _column(table, "evidence", "支撑证据")
        rows = []
        for row in table.rows:
            label = _inline_plain(table.cell(row, signal_col))
            if not label:
                continue
            tone = _signal(table.cell(row, direction))
            rows.append((label, _inline_plain(table.cell(row, direction)),
                         tone, _inline_plain(table.cell(row, evidence))[:80]))
        if rows:
            blocks.append(scorecard(rows))
    return "".join(blocks)


def research_summary(final_state: dict) -> str:
    debate = final_state.get("investment_debate_state") or {}
    bull = extract_arguments(debate.get("bull_history") or "")
    bear = extract_arguments(debate.get("bear_history") or "")
    blocks = []
    if bull or bear:
        columns = []
        for title, tone, items in (("Bull case", "up", bull), ("Bear case", "down", bear)):
            cards = "".join(
                card(item["title"], f'<p>{escape(item["summary"])}</p>', tone=tone)
                for item in items[:4]
            )
            columns.append(f'<div class="debate-side {tone}"><h4>{title}</h4>{cards}</div>')
        blocks.append('<div class="debate">' + "".join(columns) + "</div>")

    plan = final_state.get("investment_plan") or ""
    if plan:
        recommendation = re.search(r"\*\*Recommendation\*\*\s*:\s*([^\n]+)", plan, re.IGNORECASE)
        rationale = re.search(r"\*\*Rationale\*\*\s*:\s*(.+?)(?=\n\*\*|\Z)", plan,
                              re.IGNORECASE | re.DOTALL)
        actions = re.search(r"\*\*Strategic Actions\*\*\s*:\s*(.+?)(?=\n\*\*|\Z)", plan,
                            re.IGNORECASE | re.DOTALL)
        if recommendation or rationale:
            body = ""
            if rationale:
                body += f"<p>{escape(_first_sentence(rationale.group(1), 320))}</p>"
            if actions:
                body += f'<p class="muted">{escape(_first_sentence(actions.group(1), 220))}</p>'
            blocks.append(card(
                f"Research Manager · {_inline_plain(recommendation.group(1)) if recommendation else 'Decision'}",
                body, tone=_signal(recommendation.group(1) if recommendation else "")))
    return "".join(blocks)


def risk_summary(final_state: dict) -> str:
    debate = final_state.get("risk_debate_state") or {}
    sides = (("Aggressive", "up", debate.get("aggressive_history") or ""),
             ("Neutral", "neutral", debate.get("neutral_history") or ""),
             ("Conservative", "down", debate.get("conservative_history") or ""))
    cards = []
    for name, tone, text in sides:
        summary = _first_sentence(text, 260)
        if not summary:
            continue
        leads = _bullets(text, 3)
        body = f"<p>{escape(summary)}</p>"
        if leads:
            body += "<ul>" + "".join(f"<li>{escape(lead)}</li>" for lead in leads) + "</ul>"
        cards.append(card(name, body, tone=tone))
    if not cards:
        return ""
    return pills([("Aggressive", "up"), ("Neutral", "neutral"), ("Conservative", "down")]) + \
        _grid(cards, 3)


def _trade_figure(final_state: dict) -> str:
    plan = extract_trade_plan(final_state)
    if not (plan.get("entry_price_num") and plan.get("stop_loss_num")):
        return ""
    targets = [plan["price_target_num"]] if plan.get("price_target_num") else []
    return figure(
        charts.trade_plan(plan["entry_price_num"], plan["stop_loss_num"], targets,
                          title="Trade plan"),
        "<b>Entry, stop and target on one axis.</b> Red is the distance to the stop; "
        "green is the distance to the report's target.", wide=True)


def trader_summary(final_state: dict) -> str:
    plan = extract_trade_plan(final_state)
    if not plan.get("action"):
        return ""
    body = ""
    if plan.get("entry_price"):
        body += f"<p><b>Entry</b> {escape(plan['entry_price'][:100])}</p>"
    if plan.get("stop_loss"):
        body += f"<p><b>Stop</b> {escape(plan['stop_loss'][:100])}</p>"
    if plan.get("position_sizing"):
        body += f"<p class=\"muted\">{escape(plan['position_sizing'][:180])}</p>"
    return _trade_figure(final_state) + card(
        f"Trader · {plan['action']}", body, tone=_signal(plan["action"]))


def decision_summary(final_state: dict) -> str:
    text = final_state.get("final_trade_decision") or ""
    if not text:
        return ""
    plan = extract_trade_plan(final_state)
    rating = plan.get("rating") or ""
    summary = re.search(r"\*\*Executive Summary\*\*\s*:?\s*(.+?)(?=\n\*\*|\Z)", text,
                        re.IGNORECASE | re.DOTALL)
    thesis = re.search(r"\*\*Investment Thesis\*\*\s*:?\s*(.+?)(?=\n\*\*|\Z)", text,
                       re.IGNORECASE | re.DOTALL)
    target = plan.get("price_target") or "not provided"
    horizon = plan.get("time_horizon") or "not provided"
    body = ""
    if summary:
        body += f"<p>{escape(_first_sentence(summary.group(1), 360))}</p>"
    body += (f'<div class="decision-meta"><span><b>Target</b> {escape(str(target))}</span>'
             f'<span><b>Horizon</b> {escape(str(horizon))}</span></div>')
    if thesis:
        leads = _bullets(thesis.group(1), 4)
        if leads:
            body += "<ul>" + "".join(f"<li>{escape(lead)}</li>" for lead in leads) + "</ul>"
    return _trade_figure(final_state) + card(
        f"Portfolio Manager · {rating or 'Decision'}", body, tone=_signal(rating))


def agent_summary(agent: str, text: str, chart_data: dict, final_state: dict) -> str:
    """The visual block that sits above one agent's full prose."""
    if agent == "Market Analyst":
        return market_charts(chart_data) + market_summary(text, chart_data)
    if agent == "News Analyst":
        return news_summary(text)
    if agent == "Fundamentals Analyst":
        return fundamentals_summary(text)
    if agent == "Sentiment Analyst":
        return sentiment_summary(text)
    if agent == "Trader":
        return trader_summary(final_state)
    if agent == "Portfolio Manager":
        return decision_summary(final_state)
    return ""


def section_summary(heading: str, final_state: dict) -> str:
    if "Research" in heading:
        return research_summary(final_state)
    if "Risk" in heading:
        return risk_summary(final_state)
    return ""


# --------------------------------------------------------------------------- #
# dashboard
# --------------------------------------------------------------------------- #


def _levels(chart_data: dict) -> list[tuple[float, str, str]]:
    return [(float(row["price"]), str(row["label"]), str(row["kind"]))
            for row in chart_data.get("levels", []) if row.get("price") is not None]


def dashboard(chart_data: dict, final_state: dict) -> str:
    """The one-screen summary: numbers, price, levels, odds, trade plan."""
    price = chart_data.get("price") or {}
    close = price.get("close") or []
    if len(close) < 2:
        return ""
    ticker = chart_data.get("ticker", final_state.get("company_of_interest", ""))
    levels = _levels(chart_data)
    overlays = [(row["name"], row["values"], row["tone"], row["dash"])
                for row in chart_data.get("overlays", [])]
    hero = charts.price_chart(
        price["dates"], close, volume=price.get("volume"), overlays=overlays,
        bands=chart_data.get("bands"), levels=levels,
        title=f"{ticker} price, averages, Bollinger band and key levels",
        desc="Daily close against the 10 EMA, 50/200 SMA and the report's levels.",
    )
    ladder = charts.level_ladder(levels, close[-1])
    gauge = chart_data.get("gauge") or {}
    gauge_svg = charts.gauge(gauge.get("value", 0), label=gauge.get("label", ""),
                             title="RSI gauge")
    scenarios = chart_data.get("scenarios") or []
    scenario_svg = charts.prob_bars(
        [(row["label"], row["prob"], row.get("tone", "--accent")) for row in scenarios],
        title="Scenario probabilities",
    ) if scenarios else ""

    plan = extract_trade_plan(final_state)
    trade_svg = ""
    if plan.get("entry_price_num") and plan.get("stop_loss_num"):
        targets = [plan["price_target_num"]] if plan.get("price_target_num") else []
        trade_svg = charts.trade_plan(
            plan["entry_price_num"], plan["stop_loss_num"], targets,
            last=close[-1], title="Trade plan",
        )

    blocks = ['<section id="overview"><h2>At a glance</h2>']
    market_text = final_state.get("market_report") or ""
    if re.search(r"provisional|partial|incomplete|intraday|盘中|未完成|临时",
                 market_text, re.IGNORECASE):
        blocks.append('<p class="data-note">Data-quality note: the market analyst flags the '
                      'latest bar as provisional or incomplete, so the last close and the '
                      'levels derived from it may shift when the session completes.</p>')
    if chart_data.get("reconciled"):
        blocks.append('<p class="source-note">The chart\'s last bar is reconciled to the '
                      'report\'s verified close; earlier bars are the vendor series.</p>')
    blocks += [
        kpis(chart_data.get("stats", [])),
        figure(hero, "<b>Price against every average that matters.</b> The last close is "
                     "marked, with the report's own levels drawn as dashed rules; the "
                     "lower panel is volume, coloured by the day's direction.", wide=True),
        '<div class="charts pair">',
        figure(ladder, "<b>Key levels, nearest first.</b> Distance from the last close, "
                       "so the support and resistance map is one glance."),
        figure(gauge_svg, "Momentum, on the same 0–100 scale the RSI uses."),
        "</div>",
    ]
    if scenario_svg:
        blocks.append(figure(scenario_svg, "<b>The report's own odds.</b> Base case, "
                                          "failure at the supply wall, and the breakdown tail."))
    if trade_svg:
        blocks.append(figure(trade_svg, "<b>The trade plan on one axis.</b> Red is the "
                                        "distance to the stop, green the distance to the "
                                        "report's target.", wide=True))
    range_data = chart_data.get("range") or {}
    if range_data.get("low") is not None and range_data.get("high") is not None:
        blocks.append(figure(
            charts.range_bar(range_data["low"], range_data["high"], range_data["last"],
                             title="52-week range"),
            "<b>Where the last close sits in the 52-week range.</b>"))
    sentiment = extract_sentiment(final_state.get("sentiment_report") or "")
    if sentiment:
        blocks.append(figure(
            charts.gauge(sentiment["score"] * 10,
                         label=f"{sentiment['band']} · {sentiment['score']:.1f}/10"),
            "<b>Community sentiment.</b> The report's own 0–10 score, on the same "
            "0–100 scale as RSI."))
    blocks.append("</section>")
    return "".join(blocks)


def _report_number(text: str, label: str, window: int = 18) -> float | None:
    # Prefer the table row (``10 EMA | 184.82``) over a narrative "from X to Y".
    table = re.search(rf"{label}\s*\|\s*([-+\u2212]?[\d,]+(?:\.\d+)?)",
                      text or "", re.IGNORECASE)
    if table:
        return number(table.group(1))
    match = re.search(rf"{label}[^0-9]{{0,{window}}}([-+\u2212]?[\d,]+(?:\.\d+)?)",
                      text or "", re.IGNORECASE)
    return number(match.group(1)) if match else None


def _report_volume(text: str) -> float | None:
    text = text or ""
    # Chinese reports often write "234.9 万股" rather than a raw share count.
    match = re.search(r"成交量(?:仅|只有)?[^0-9]{0,12}([\d,.]+)\s*万\s*股", text)
    if match:
        value = number(match.group(1))
        if value is not None:
            return value * 1e4
    # A dated OHLCV table row is the most exact source when it exists.
    match = re.search(
        r"\|\s*\d{1,2}-\d{1,2}\s*\|[^|]*\|[^|]*\|[^|]*\|\s*([\d,]+)\s*\|", text)
    if match:
        value = number(match.group(1))
        if value is not None:
            return value
    match = re.search(r"成交量[：:\s]*([\d,]+)\s*股", text)
    if match:
        value = number(match.group(1))
        if value is not None:
            return value
    for pattern in (
        r"volume is only\s*\**([\d,.]+)\s*([KMB])?",
        r"volume[:\s]+\**([\d,.]+)\s*([KMB])?",
    ):
        match = re.search(pattern, text, re.IGNORECASE)
        if not match:
            continue
        value = number(match.group(1))
        if value is None:
            continue
        suffix = (match.group(2) or "").upper() if match.lastindex and match.lastindex >= 2 else ""
        return value * {"K": 1e3, "M": 1e6, "B": 1e9}.get(suffix, 1)
    match = re.search(r"([\d,.]+)\s*万\s*股", text)
    if match:
        value = number(match.group(1))
        if value is not None:
            return value * 1e4
    return None


def _bollinger(text: str) -> tuple[float | None, float | None, float | None]:
    match = re.search(
        r"Bollinger[^\n]{0,120}?middle\s*([\d,.]+)[^\n]{0,60}?upper\s*([\d,.]+)"
        r"[^\n]{0,60}?lower\s*([\d,.]+)", text or "", re.IGNORECASE)
    if not match:
        return None, None, None
    return number(match.group(1)), number(match.group(2)), number(match.group(3))


def _macd_values(text: str) -> tuple[float | None, float | None, float | None]:
    match = re.search(
        r"MACD\s*\(line\s*([-+\u2212]?[\d,.]+),\s*signal\s*([-+\u2212]?[\d,.]+),"
        r"\s*histogram\s*([-+\u2212]?[\d,.]+)\)", text or "", re.IGNORECASE)
    if not match:
        return None, None, None
    return number(match.group(1)), number(match.group(2)), number(match.group(3))


def reconcile_chart_data(data: dict, market_text: str) -> dict:
    """Make the chart's last bar agree with the report's verified snapshot.

    A vendor can restate a historical bar (or serve a partial one), so the
    report's own "last verified close" is the source of truth. Earlier bars stay
    the vendor series; only the final point and the summary numbers are moved.
    """
    price = data.get("price") or {}
    close = price.get("close") or []
    if len(close) < 2:
        return data
    last = _report_number(market_text, "last verified close") or \
        _report_number(market_text, "last close")
    if last is None:
        match = re.search(r"\|\s*(?:Close|收盘(?:价)?)\s*\|\s*([\d,]+(?:\.\d+)?)",
                          market_text or "", re.IGNORECASE)
        last = number(match.group(1)) if match else None
    if last is None:
        # "| 开盘 / 最高 / 最低 / 收盘 | 167.35 / 171.70 / 163.72 / 164.31 |"
        match = re.search(
            r"\|\s*[^|]*(?:开盘[^|]*收盘|Close\s*\()[^|]*\|\s*([^|]+)\|",
            market_text or "", re.IGNORECASE)
        if match:
            values = re.findall(r"[\d,]+(?:\.\d+)?", match.group(1))
            last = number(values[-1]) if values else None
    if last is None or not 0 < last < 1_000_000:
        return data
    last = round(last, 2)
    if abs(float(close[-1]) - last) < 0.01:
        return data

    close[-1] = last
    volume = price.get("volume") or []
    report_volume = _report_volume(market_text)
    if report_volume and volume:
        volume[-1] = int(report_volume)

    # Indicators the report states explicitly.
    rsi = _report_number(market_text, "RSI")
    atr = _report_number(market_text, "ATR")
    if rsi is not None and data.get("rsi", {}).get("values"):
        data["rsi"]["values"][-1] = round(rsi, 1)
    macd, signal, histogram = _macd_values(market_text)
    if macd is not None and data.get("macd", {}).get("macd"):
        data["macd"]["macd"][-1] = macd
        data["macd"]["signal"][-1] = signal
        data["macd"]["histogram"][-1] = histogram

    references: dict[str, float] = {}
    for name in ("10 EMA", "50 SMA", "200 SMA", "VWMA"):
        value = _report_number(market_text, name)
        if value is not None:
            references[name] = round(value, 2)
            for overlay in data.get("overlays", []):
                if overlay.get("name") == name and overlay.get("values"):
                    overlay["values"][-1] = round(value, 2)
    boll_mid, boll_upper, boll_lower = _bollinger(market_text)
    if boll_mid is not None:
        references["BB mid"] = round(boll_mid, 2)
    if boll_lower is not None:
        references["BB lower"] = round(boll_lower, 2)
    bands = data.get("bands") or {}
    if boll_upper is not None and bands.get("upper"):
        bands["upper"][-1] = round(boll_upper, 2)
    if boll_lower is not None and bands.get("lower"):
        bands["lower"][-1] = round(boll_lower, 2)

    # Recompute the derived numbers the cards and charts read.
    previous = close[-2]
    change = (last - previous) / previous * 100 if previous else 0.0
    range_data = data.get("range") or {}
    high = range_data.get("high")
    drawdown = (last - high) / high * 100 if high else 0.0
    sma50 = references.get("50 SMA")
    sma200 = references.get("200 SMA")
    gap = (sma50 - sma200) if sma50 is not None and sma200 is not None else None
    recent = [v for v in volume[-20:] if v]
    average_volume = sum(recent) / len(recent) if recent else 0
    volume_ratio = volume[-1] / average_volume if average_volume and volume else 0
    rsi_label = ("oversold" if rsi is not None and rsi < 30 else
                 "overbought" if rsi is not None and rsi > 70 else "neutral zone")
    if rsi is not None:
        data["gauge"] = {"value": round(rsi, 1), "label": f"RSI · {rsi_label}"}

    for item in data.get("stats", []):
        label = item.get("label")
        if label == "Last close":
            item["value"] = _fmt(last)
            item["note"] = price.get("dates", [""])[-1]
        elif label == "Day":
            item["value"] = _pct(change, 2, signed=True)
            item["tone"] = "up" if change >= 0 else "down"
        elif label == "RSI (14)" and rsi is not None:
            item["value"] = f"{rsi:.1f}"
            item["note"] = rsi_label
            item["tone"] = "down" if rsi > 70 else "up" if rsi < 30 else ""
        elif label == "ATR (14)" and atr is not None:
            item["value"] = _fmt(atr)
            item["note"] = f"{atr / last * 100:.2f}% of price"
        elif label == "From 52w high" and high:
            item["value"] = _pct(drawdown, 1, signed=True)
            item["note"] = f"high {_fmt(high)}"
            item["tone"] = "down" if drawdown < -10 else ""
        elif label == "50/200 gap" and gap is not None and sma200:
            item["value"] = f"{gap:+.2f}".replace("-", "\u2212")
            item["note"] = f"{gap / sma200 * 100:+.2f}%".replace("-", "\u2212")
            item["tone"] = "down" if gap < 0 else "up"
        elif label == "Volume" and volume:
            item["value"] = f"{volume[-1] / 1e6:,.1f}M"
            item["note"] = f"{volume_ratio:.1f}x 20d avg"

    for row in data.get("distances", []):
        reference = references.get(row.get("label"))
        if reference:
            row["value"] = round((last - reference) / reference * 100, 2)
    generic = {"10 ema", "50 sma", "200 sma", "vwma", "bb mid", "bb lower"}
    by_price: dict[float, dict] = {}
    for level in data.get("levels", []):
        reference = references.get(level.get("label"))
        if reference:
            level["price"] = round(reference, 2)
            level["kind"] = "support" if reference < last else "resistance"
        key = round(level.get("price", 0), 2)
        existing = by_price.get(key)
        if existing is None or (existing.get("label", "").lower() in generic
                                and level.get("label", "").lower() not in generic):
            by_price[key] = level
    data["levels"] = list(by_price.values())

    data["reconciled"] = True
    return data


def build_chart_data_for_report(ticker: str, final_state: dict) -> dict:
    """Build the price/indicator payload, or ``{}`` when the data is unavailable."""
    trade_date = final_state.get("trade_date")
    if not trade_date:
        return {}
    try:
        texts = [final_state.get("market_report") or "",
                 final_state.get("trader_investment_plan") or "",
                 final_state.get("final_trade_decision") or ""]
        levels = extract_levels(texts)
        scenarios = extract_scenarios(final_state.get("market_report") or "")
        from tradingagents.chart_data import build_chart_data
        data = build_chart_data(ticker, trade_date, levels=levels, scenarios=scenarios)
        return reconcile_chart_data(data, final_state.get("market_report") or "")
    except Exception:
        # A missing chart must never stop a report from being written.
        return {}
