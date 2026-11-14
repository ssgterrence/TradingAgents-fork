"""The report as one self-contained HTML page (#1419).

The page reads well in a browser, on a phone and in print. It loads nothing and
runs nothing: styles are inline, there is no script, and a Content-Security-Policy
forbids any fetch. Report text is rendered as CommonMark with raw HTML and images
off, so nothing a model wrote can inject markup or load a remote asset.
"""

from datetime import datetime
from html import escape
from importlib.resources import files

from markdown_it import MarkdownIt

from tradingagents import report_visuals as visuals
from tradingagents.agents.rating import run_rating
from tradingagents.reporting import analyst_names

# Ratings by direction, so the page can show which way the call leans.
_TONE = {"Buy": "up", "Overweight": "up", "Hold": "level", "Underweight": "down", "Sell": "down"}

# The Tauric Research logo as published (tauric.ai/brand/tauric-logo.svg), drawn
# in the page so it loads nothing.
_LOGO = files("tradingagents").joinpath("assets/tauric-logo.svg").read_text(encoding="utf-8").strip()
_COMPANY = "https://tauric.ai"
_ORG = "https://github.com/TauricResearch"
_PROJECT = f"{_ORG}/TradingAgents"

_CSS = """
:root {
  --paper: #fbfbfa; --ink: #1c2126; --muted: #5d6670; --rule: #e2e5e8; --wash: #f2f4f5;
  --accent: #087a59; --up: #087a59; --down: #b4372f; --level: #5d6670; --edge: #d3d8dc; --mark: #878f97;
  --serif: Charter, "Bitstream Charter", "Sitka Text", Cambria, Georgia, serif;
  --sans: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  color-scheme: light dark;
}
@media (prefers-color-scheme: dark) {
  :root {
    --paper: #131a1f; --ink: #e4e8eb; --muted: #9aa6af; --rule: #263239; --wash: #1a242a;
    --accent: #14c290; --up: #14c290; --down: #ef6f63; --level: #9aa6af; --edge: #3d4c55; --mark: #66737c;
  }
}
@media (prefers-color-scheme: dark) {
  .masthead .logo [stroke="#363636"] { stroke: var(--muted); }
}
* { box-sizing: border-box; }
html { -webkit-text-size-adjust: 100%; }
body {
  margin: 0; background: var(--paper); color: var(--ink);
  font: 17px/1.62 var(--serif); font-kerning: normal;
}
.page { max-width: 46rem; margin: 0 auto; padding: 3.5rem 1.5rem 6rem; }
main h2, main h3 { scroll-margin-top: 1rem; }
a { color: var(--accent); text-underline-offset: 0.15em; }
h1, h2, h3, h4 { text-wrap: balance; }
a:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }

.masthead { padding-bottom: 1.75rem; border-bottom: 1px solid var(--rule); }
/* The logo leads at the top left, where readers look for it, 24px tall (the usual
   on-screen floor for a wordmark) with at least its height clear below. */
.masthead .logo { display: block; width: fit-content; margin: 0 0 2.25rem; }
.masthead .logo svg { display: block; height: 1.5rem; width: auto; }
.masthead h1 {
  margin: 0; font: 600 2.6rem/1.1 var(--sans); letter-spacing: -0.02em;
  display: flex; flex-wrap: wrap; align-items: baseline; gap: 0.2em 0.5em;
}
.masthead .rating { font-weight: 500; }
.rating.up { color: var(--up); } .rating.down { color: var(--down); } .rating.level { color: var(--level); }
.rating.review { color: var(--muted); font-style: italic; }
.masthead .date { margin: 0.55rem 0 1.5rem; font: 1rem/1.4 var(--sans); color: var(--muted); }
.run { margin: 0; display: grid; grid-template-columns: max-content 1fr; gap: 0.45rem 1.25rem;
  font: 0.85rem/1.5 var(--sans); }
.run > div { display: contents; }
.run dt { color: var(--muted); }
.run dd { margin: 0; overflow-wrap: anywhere; }
.run .note dd { color: var(--down); }
.field { display: inline-block; margin: 0 0.15rem 0.15rem 0; padding: 0 0.4rem; border: 1px solid var(--edge);
  border-radius: 4px; background: var(--wash); font: 0.8rem/1.6 ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }
.run .group { display: inline-block; margin-right: 0.9rem; white-space: nowrap; }
.run .group > .name { color: var(--muted); margin-right: 0.3rem; }
.run .then { color: var(--muted); margin: 0 0.2rem; }

/* The sections: listed under the header on narrow screens. On wide ones, a
   quiet rail centred on the left edge (numerals for the sections, short bars
   for their agents) that opens into the full list when pointed at or focused. */
.contents { margin: 2.25rem 0 0; font: 0.9rem/1.45 var(--sans); }
.contents ul { margin: 0; padding: 0; list-style: none; }
.contents > ul > li { margin: 0 0 0.75rem; }
.contents ul ul { margin-top: 0.2rem; padding-left: 1.6rem; font-size: 0.85rem; }
.contents ul ul li { margin: 0.1rem 0; }
.contents a { display: flex; align-items: center; gap: 0.6rem; color: var(--muted); text-decoration: none; }
.contents > ul > li > a { color: var(--ink); }
.contents .num { min-width: 1.6rem; color: var(--muted); font-variant-numeric: tabular-nums; }
.contents .bar { display: none; }
.contents a:hover .label, .contents a:focus-visible .label { color: var(--accent); text-decoration: underline; }
.to-top { position: fixed; right: 1rem; bottom: calc(1rem + env(safe-area-inset-bottom));
  padding: 0.25rem 0.6rem; border: 1px solid var(--edge); border-radius: 4px; background: var(--paper);
  color: var(--muted); font: 0.8rem/1.4 var(--sans); text-decoration: none; }

@media (min-width: 60rem) {
  .contents { position: fixed; left: 1rem; top: 50%; transform: translateY(-50%); z-index: 1;
    max-height: 86vh; overflow-y: auto; overscroll-behavior: contain; margin: 0;
    padding: 0.7rem 0.9rem; border: 1px solid transparent; border-radius: 6px;
    transition: background-color 0.15s, border-color 0.15s, box-shadow 0.15s; }
  .contents > ul > li { margin: 0 0 0.35rem; }
  .contents ul ul { margin-top: 0; padding-left: 0; }
  .contents ul ul li { margin: 0; }
  /* Marks reach 3:1 contrast and rows 24px, the WCAG 2.2 floors for a control's
     visual cue and its pointer target. */
  .contents a { min-height: 1.5rem; }
  .contents .num { min-width: 1.4rem; }
  .contents .bar { display: block; flex: none; width: 1.25rem; height: 2px; margin-left: 0.2rem;
    border-radius: 1px; background: var(--mark); }
  .contents .label { max-width: 0; opacity: 0; overflow: hidden; white-space: nowrap;
    transition: opacity 0.15s, max-width 0.2s; }
  .contents:hover, .contents:focus-within { background: var(--paper); border-color: var(--rule);
    box-shadow: 0 6px 24px rgb(0 0 0 / 0.08); }
  .contents:hover .label, .contents:focus-within .label { max-width: 18rem; opacity: 1; }
  .contents a:hover .bar, .contents a:focus-visible .bar { background: var(--accent); }
  .to-top { display: none; }
}
@media (prefers-reduced-motion: reduce) {
  .contents, .contents .label { transition: none; }
}

/* The maker's credit: one quiet line at the foot. */
.credit { margin-top: 4.5rem; padding-top: 1.25rem; border-top: 1px solid var(--rule);
  color: var(--muted); font: 0.8rem/1.4 var(--sans); }
.credit a { color: inherit; text-decoration: none; }
.credit a.brand { color: var(--accent); }
.credit a:hover, .credit a:focus-visible { text-decoration: underline; }

/* Visual summaries: the page leads with cards and charts, and the full prose
   stays one click away. Everything here is plain HTML/CSS and inline SVG. */
.visual-summary { margin: 0 0 1.5rem; }
.visual-summary:empty { display: none; }
.vheading { margin: 1.5rem 0 0.6rem; font: 600 0.95rem/1.4 var(--sans); }
.muted { color: var(--muted); }
.data-note { margin: 0 0 1rem; padding: 0.55rem 0.8rem; border-left: 3px solid var(--down);
  background: var(--wash); color: var(--muted); font: 0.82rem/1.5 var(--sans); border-radius: 0 4px 4px 0; }
.source-note { margin: 0 0 1rem; color: var(--muted); font: 0.76rem/1.5 var(--sans); }

.vgrid { display: grid; gap: 0.65rem; margin: 0 0 1.25rem; }
.vgrid.cols-2 { grid-template-columns: repeat(auto-fit, minmax(15rem, 1fr)); }
.vgrid.cols-3 { grid-template-columns: repeat(auto-fit, minmax(12rem, 1fr)); }
.vcard { padding: 0.8rem 0.9rem; border: 1px solid var(--rule); border-radius: 6px;
  background: var(--wash); }
.vcard.up { border-left: 3px solid var(--up); }
.vcard.down { border-left: 3px solid var(--down); }
.vcard.watch { border-left: 3px solid var(--mark); }
.vcard.neutral { border-left: 3px solid var(--edge); }
.vcard-title { font: 600 0.92rem/1.35 var(--sans); margin-bottom: 0.35rem; }
.vcard-meta { font: 0.72rem/1.35 var(--sans); color: var(--muted); text-transform: uppercase;
  letter-spacing: 0.04em; margin-bottom: 0.25rem; }
.vcard-body p { margin: 0 0 0.45rem; font: 0.86rem/1.5 var(--sans); }
.vcard-body p:last-child { margin-bottom: 0; }
.vcard-body ul { margin: 0.25rem 0 0; padding-left: 1.1rem; font: 0.84rem/1.5 var(--sans); }
.vcard-body li { margin: 0.15rem 0; }

.scorecard { margin: 0 0 1.25rem; border: 1px solid var(--rule); border-radius: 6px;
  overflow: hidden; font: 0.82rem/1.4 var(--sans); }
.score-head, .score-row { display: grid; grid-template-columns: 1.1fr 0.7fr 0.8fr 1.6fr;
  gap: 0.5rem; align-items: baseline; padding: 0.4rem 0.7rem; }
.scorecard:where([data-cols="3"]) .score-head,
.scorecard:where([data-cols="3"]) .score-row { grid-template-columns: 0.9fr 1fr 2.2fr; }
.scorecard:where([data-cols="2"]) .score-head,
.scorecard:where([data-cols="2"]) .score-row { grid-template-columns: 0.8fr 2.4fr; }
.scorecard:where([data-cols="1"]) .score-head,
.scorecard:where([data-cols="1"]) .score-row { grid-template-columns: 1fr; }
.score-head { background: var(--wash); color: var(--muted); font-weight: 600;
  text-transform: uppercase; letter-spacing: 0.04em; font-size: 0.7rem; }
.score-row { border-top: 1px solid var(--rule); }
.score-label { font-weight: 600; }
.score-value { font-variant-numeric: tabular-nums; }
.score-signal { font-weight: 600; }
.score-signal.up { color: var(--up); }
.score-signal.down { color: var(--down); }
.score-signal.watch { color: var(--mark); }
.score-signal.neutral { color: var(--muted); }
.score-note { color: var(--muted); font-size: 0.78rem; }

.pills { display: flex; flex-wrap: wrap; gap: 0.4rem; margin: 0 0 1rem; }
.pill { padding: 0.15rem 0.55rem; border: 1px solid var(--edge); border-radius: 999px;
  font: 0.75rem/1.5 var(--sans); color: var(--muted); background: var(--wash); }
.pill.up { border-color: var(--up); color: var(--up); }
.pill.down { border-color: var(--down); color: var(--down); }
.pill.neutral { border-color: var(--edge); }

.timeline { list-style: none; margin: 0 0 1.25rem; padding: 0; border-left: 2px solid var(--rule); }
.timeline li { position: relative; padding: 0 0 0.65rem 1rem; font: 0.84rem/1.45 var(--sans); }
.timeline li::before { content: ""; position: absolute; left: -5px; top: 0.35rem; width: 8px;
  height: 8px; border-radius: 50%; background: var(--accent); }
.timeline .when { display: block; color: var(--accent); font-weight: 600; font-size: 0.78rem; }
.timeline .what { color: var(--muted); }

.debate { display: grid; grid-template-columns: repeat(auto-fit, minmax(16rem, 1fr));
  gap: 1rem; margin: 0 0 1.5rem; }
.debate-side h4 { margin: 0 0 0.5rem; font: 600 0.9rem/1.4 var(--sans); }
.debate-side.up h4 { color: var(--up); }
.debate-side.down h4 { color: var(--down); }
.debate-side .vcard { margin-bottom: 0.5rem; }
.decision-meta { display: flex; flex-wrap: wrap; gap: 1rem; margin: 0.5rem 0;
  font: 0.82rem/1.4 var(--sans); color: var(--muted); }
.decision-meta b { color: var(--ink); }

/* The full prose is collapsed by default; print forces it open. */
.full-text { margin: 1.25rem 0 0; padding-top: 0.65rem; border-top: 1px solid var(--rule); }
.full-text > summary { cursor: pointer; color: var(--muted); font: 0.82rem/1.4 var(--sans);
  list-style: none; display: flex; align-items: center; gap: 0.4rem; }
.full-text > summary::-webkit-details-marker { display: none; }
.full-text > summary::before { content: "▸"; color: var(--accent); font-size: 0.8rem; }
.full-text[open] > summary::before { content: "▾"; }
.full-text > summary:hover { color: var(--accent); }
.full-text .prose { margin-top: 0.9rem; }
.full-text .prose > :first-child { margin-top: 0; }

@media (max-width: 40rem) {
  .scorecard .score-head, .scorecard .score-row {
    grid-template-columns: minmax(0, 1fr) minmax(0, 1.5fr); }
  .score-signal { display: none; }
  .score-note { grid-column: 1 / -1; display: block; }
  .scorecard .score-head > .score-h-signal,
  .scorecard .score-head > .score-h-note { display: none; }
}

/* Three levels of separation: the five groups, the agents within a group, and
   breaks an agent draws inside its own text. */
main h2 {
  margin: 4.5rem 0 0.25rem; padding-top: 1.5rem; border-top: 2px solid var(--ink);
  font: 600 1.45rem/1.3 var(--sans); letter-spacing: -0.01em;
}
main section:first-child h2 { margin-top: 3rem; }
main h3 { margin: 2.75rem 0 0.75rem; padding-top: 1.1rem; border-top: 1px solid var(--rule);
  font: 600 1.15rem/1.35 var(--sans); color: var(--accent); }
main h2 + h3 { margin-top: 1.25rem; padding-top: 0; border-top: 0; }
main h4, main h5, main h6 { margin: 1.75rem 0 0.5rem; font: 600 1rem/1.4 var(--sans); }
main h5, main h6 { color: var(--muted); }
main p, main ul, main ol { margin: 0 0 1rem; }
main li { margin: 0.25rem 0; }
main strong { font-weight: 650; }
main blockquote { margin: 1.25rem 0; padding: 0.1rem 0 0.1rem 1rem; border-left: 3px solid var(--rule);
  color: var(--muted); }
main code { font: 0.88em/1.4 ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  background: var(--wash); padding: 0.1em 0.3em; border-radius: 3px; }
main pre { background: var(--wash); padding: 0.9rem 1rem; border-radius: 4px; overflow-x: auto; }
main pre code { background: none; padding: 0; }
main hr { width: 3rem; margin: 2rem auto; border: 0; border-top: 1px solid var(--rule); }

.table { overflow-x: auto; margin: 0 0 1.25rem; }
table { border-collapse: collapse; width: 100%; font: 0.86rem/1.45 var(--sans);
  font-variant-numeric: tabular-nums; }
th, td { padding: 0.45rem 0.7rem; text-align: left; vertical-align: top; border-bottom: 1px solid var(--rule); }
th { font-weight: 600; border-bottom-color: var(--muted); }
tbody tr:last-child td { border-bottom: 0; }

/* Charts are inline SVG: one palette, no script, no remote asset. */
.chart { max-width: 34rem; margin: 0 auto 1.75rem; }
.chart.wide { max-width: none; }
.chart .plot { overflow-x: auto; overscroll-behavior-x: contain; }
.chart svg { display: block; width: 100%; height: auto; overflow: visible; }
.chart figcaption { margin-top: 0.45rem; font: 0.82rem/1.45 var(--sans); color: var(--muted); }
.chart figcaption b { color: var(--ink); font-weight: 600; }
.scroll-hint { display: none; }
.charts.pair { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 0.62fr);
  gap: 1.25rem; align-items: start; margin: 0 0 1.75rem; max-width: 44rem; }
.charts.pair .chart { max-width: none; margin: 0; }
.chart-svg text { font-kerning: normal; }
.c-grid { stroke: var(--rule); stroke-width: 1; }
.c-axis { fill: var(--muted); font-variant-numeric: tabular-nums; }
.c-price { stroke: var(--ink); }
.c-overlay { fill: none; }
.c-indicator { stroke: var(--accent); fill: none; }
.c-indicator-dot { fill: var(--accent); }
.c-dot { fill: var(--ink); }
.c-dot-support { fill: var(--up); }
.c-dot-resistance { fill: var(--down); }
.c-level { stroke: var(--muted); stroke-width: 0.8; }
.c-level-support { stroke: var(--up); stroke-width: 0.9; stroke-dasharray: 4 4; opacity: 0.75; }
.c-level-resistance { stroke: var(--down); stroke-width: 0.9; stroke-dasharray: 4 4; opacity: 0.75; }
.c-band { fill: var(--accent); opacity: 0.08; }
.c-volume-up { fill: var(--up); opacity: 0.35; }
.c-volume-down { fill: var(--down); opacity: 0.35; }
.c-zone-up { fill: var(--up); opacity: 0.06; }
.c-zone-down { fill: var(--down); opacity: 0.06; }
.c-gauge-track { stroke: var(--rule); }
.c-gauge-up { stroke: var(--up); opacity: 0.55; }
.c-gauge-down { stroke: var(--down); opacity: 0.55; }
.c-needle { stroke: var(--ink); stroke-width: 2; stroke-linecap: round; }
.c-bar-up { fill: var(--up); opacity: 0.75; }
.c-bar-down { fill: var(--down); opacity: 0.75; }
.c-track { fill: var(--wash); stroke: var(--rule); stroke-width: 0.6; }
.c-current-row { fill: var(--wash); }

/* The one-screen summary: six numbers, then the hero chart. */
.kpis { display: grid; grid-template-columns: repeat(auto-fit, minmax(9.5rem, 1fr));
  gap: 0.6rem; margin: 1.1rem 0 1.6rem; }
.kpi { padding: 0.65rem 0.8rem; border: 1px solid var(--rule); border-radius: 6px; background: var(--wash); }
.kpi .value { font: 600 1.3rem/1.2 var(--sans); font-variant-numeric: tabular-nums; }
.kpi.text .value { font: 600 0.92rem/1.35 var(--sans); }
.kpi .label { font: 0.7rem/1.35 var(--sans); letter-spacing: 0.05em; text-transform: uppercase;
  color: var(--muted); }
.kpi .note { font: 0.75rem/1.35 var(--sans); color: var(--muted); }
.kpi.up .value { color: var(--up); }
.kpi.down .value { color: var(--down); }

@media (max-width: 34rem) {
  body { font-size: 16px; }
  .page { padding: 2rem 1rem 3rem; }
  .masthead h1 { font-size: 2rem; }
  .masthead .logo svg { height: 1.25rem; }
  .run { grid-template-columns: 1fr; gap: 0 0; }
  .run dd { margin-bottom: 0.45rem; }
  .run .group { white-space: normal; }
}
@media (max-width: 48rem) {
  .charts.pair { grid-template-columns: 1fr; }
  /* The wide panels keep a readable scale and scroll sideways instead of
     shrinking 9px labels to 5px. */
  .chart.wide .plot svg { min-width: 44rem; }
  .scroll-hint { display: inline; color: var(--muted); }
  .charts.pair > .chart + .chart { max-width: 20rem; margin-inline: auto; }
}
@media print {
  :root { --paper: #fff; --ink: #000; --muted: #444; --rule: #bbb; --accent: #000; --wash: #f2f2f2;
    --edge: #bbb; --up: #087a59; --down: #b4372f; --level: #444; }
  body { font-size: 11pt; }
  .table { overflow: visible; }
  .page { max-width: none; padding: 0; }
  .contents, .to-top { display: none; }
  main h2 { break-before: page; border-top: 0; margin-top: 0; }
  main section:first-child h2 { break-before: auto; }
  main h3, main h4 { break-after: avoid; }
  a { color: inherit; text-decoration: none; }
  table { break-inside: avoid; }
  .chart { break-inside: avoid; }
  .full-text > summary { display: none; }
  .full-text > .prose { display: block !important; }
}
"""


def _markdown() -> MarkdownIt:
    md = MarkdownIt("commonmark", {"html": False}).enable("table").disable("image")
    md.add_render_rule("table_open", lambda *a: '<div class="table"><table>\n')
    md.add_render_rule("table_close", lambda *a: "</table></div>\n")
    return md


def _render_agent_text(md: MarkdownIt, text: str) -> str:
    """An agent's text, its own headings placed below the agent's heading (h3)."""
    tokens = md.parse(text)
    for token in tokens:
        if token.type in ("heading_open", "heading_close"):
            token.tag = f"h{min(int(token.tag[1]) + 3, 6)}"
    return md.renderer.render(tokens, md.options, {})


# What each data category serves, as a reader would name it.
_CATEGORY = {
    "core_stock_apis": "Prices", "technical_indicators": "Indicators", "fundamental_data": "Fundamentals",
    "news_data": "News", "macro_data": "Macro", "prediction_markets": "Prediction markets",
}


def _fields(values) -> str:
    return " ".join(f'<span class="field">{escape(str(v))}</span>' for v in values)


def _chain(vendors: str) -> str:
    """A vendor chain in the order it is tried: ``a,b`` reads a, then b."""
    names = [v.strip() for v in str(vendors).split(",") if v.strip()]
    return ' <span class="then">\u2192</span> '.join(_fields([n]) for n in names)


def _group(name: str, values_html: str) -> str:
    return f'<span class="group"><span class="name">{escape(name)}</span>{values_html}</span>'


def _run_details(final_state: dict, settings: dict | None) -> list[tuple[str, str]]:
    """The run details as (label, value HTML); every value from the run is escaped."""
    generated = final_state.get("generated_at") or datetime.now().strftime("%Y-%m-%d %H:%M")
    details = [("Generated", escape(generated))]
    if settings:
        s = settings.get
        for tier in ("deep", "quick"):
            provider = s(f"{tier}_think_provider") or s("llm_provider", "?")
            details.append((f"{tier.capitalize()} model", _fields([provider, s(f"{tier}_think_llm", "?")])))
        details.append(("Analysts", _fields(analyst_names(s("analysts")))))
        details.append(("Debate rounds", " ".join((
            _group("research", _fields([s("max_debate_rounds", "?")])),
            _group("risk", _fields([s("max_risk_discuss_rounds", "?")])),
        ))))
        vendors = {**(s("data_vendors") or {}), **(s("tool_vendors") or {})}
        if vendors:
            details.append(("Data vendors", " ".join(
                _group(_CATEGORY.get(k, k), _chain(v)) for k, v in vendors.items()
            )))
        details.append(("Version", escape(f"TradingAgents {s('version', '?')}")))
    if final_state.get("memory_note"):
        details.append(("Memory log", escape(final_state["memory_note"])))
    return details


def render_report(ticker: str, final_state: dict, settings: dict | None, parts,
                  chart_data: dict | None = None) -> str:
    """The report page: title and rating, what produced the run, contents, sections."""
    md = _markdown()
    rating = run_rating(final_state) if final_state.get("final_trade_decision") else ""
    tone = _TONE.get(rating, "review")
    date = final_state.get("trade_date", "")

    title = f'<span class="ticker">{escape(ticker)}</span>'
    if rating:
        title += f' <span class="rating {tone}">{escape(rating)}</span>'
    details = "".join(
        f'<div class="{"note" if label == "Memory log" else "detail"}">'
        f"<dt>{escape(label)}</dt><dd>{value}</dd></div>"
        for label, value in _run_details(final_state, settings)
    )

    contents, body = [], []
    chart_data = chart_data if chart_data is not None else (final_state.get("chart_data") or {})
    overview = visuals.dashboard(chart_data, final_state)
    if overview:
        contents.append('<li><a href="#overview"><span class="num">0</span> '
                        '<span class="label">At a glance</span></a></li>')
        body.append(overview)
    for n, (heading, _folder, written) in enumerate(parts, 1):
        agents = "".join(
            f'<li><a href="#s{n}-{m}"><span class="bar"></span> <span class="label">{escape(agent)}</span></a></li>'
            for m, (agent, _f, _t) in enumerate(written, 1)
        )
        numeral, _, name = heading.partition(". ")
        contents.append(f'<li><a href="#s{n}"><span class="num">{escape(numeral)}</span> '
                        f'<span class="label">{escape(name)}</span></a><ul>{agents}</ul></li>')
        body.append(f'<section id="s{n}"><h2>{escape(heading)}</h2>')
        summary = visuals.section_summary(heading, final_state)
        if summary:
            body.append(f'<div class="visual-summary">{summary}</div>')
        for m, (agent, _filename, text) in enumerate(written, 1):
            body.append(f'<h3 id="s{n}-{m}">{escape(agent)}</h3>')
            agent_visuals = visuals.agent_summary(agent, text, chart_data, final_state)
            if agent_visuals:
                body.append(f'<div class="visual-summary">{agent_visuals}</div>')
            minutes = max(1, round(len((text or "").split()) / 230))
            body.append(
                f'<details class="full-text" id="full-s{n}-{m}">'
                f'<summary>Read the full {escape(agent)} analysis · {minutes} min</summary>'
                f'<div class="prose">{_render_agent_text(md, text)}</div></details>'
            )
        body.append("</section>")

    page_title = " ".join(x for x in (ticker, date, rating) if x)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'">
<title>{escape(page_title)}: TradingAgents report</title>
<style>{_CSS}</style>
</head>
<body>
<div class="page" id="top">
<header class="masthead">
<a class="logo" href="{_COMPANY}" rel="noopener" aria-label="Tauric Research">{_LOGO}</a>
<h1>{title}</h1>
<p class="date">{escape(f"Analysis of {date}" if date else "Analysis")}</p>
<dl class="run">{details}</dl>
</header>
<nav class="contents" aria-label="Sections"><ul>{"".join(contents)}</ul></nav>
<main>
{"".join(body)}
</main>
<footer class="credit"><a href="{_PROJECT}" rel="noopener">TradingAgents</a> powered by <a class="brand" href="{_ORG}" rel="noopener">Tauric Research</a></footer>
</div>
<a class="to-top" href="#top">Top</a>
</body>
</html>
"""
