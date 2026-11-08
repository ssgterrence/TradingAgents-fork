"""Reusable report-tree writer shared by the CLI and the programmatic API.

Writes a run's per-section markdown (analysts, research, trading, risk,
portfolio) plus a consolidated ``complete_report.md`` under ``save_path``. The
CLI and ``TradingAgentsGraph.save_reports`` both call this, so a headless / API
run produces the same on-disk report tree a CLI run does.
"""

import re
from datetime import datetime
from pathlib import Path

from tradingagents.agents.rating import run_rating
from tradingagents.dataflows.quality import render_markdown as render_data_quality


def analyst_names(keys) -> list[str]:
    """The analysts as users select them: the sentiment analyst's key is "social"."""
    return ["sentiment" if key == "social" else key for key in keys or []]


def _header(ticker: str, final_state: dict, settings: dict | None) -> str:
    """The report's title and what produced it: analysis date, version, models, analysts, vendors."""
    lines = [f"# Trading Analysis Report: {ticker}", ""]
    if final_state.get("trade_date"):
        lines.append(f"- Analysis date: {final_state['trade_date']}")
    if final_state.get("final_trade_decision"):
        lines.append(f"- Rating: {run_rating(final_state)}")
    lines.append(f"- Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    if settings:
        s = settings.get
        deep_provider = s("deep_think_provider") or s("llm_provider", "?")
        quick_provider = s("quick_think_provider") or s("llm_provider", "?")
        if deep_provider == quick_provider:
            models = f"{deep_provider}, deep {s('deep_think_llm', '?')}, quick {s('quick_think_llm', '?')}"
        else:   # each tier on its own provider (#1440)
            models = (f"deep {deep_provider} {s('deep_think_llm', '?')}, "
                      f"quick {quick_provider} {s('quick_think_llm', '?')}")
        lines.append(f"- TradingAgents {s('version', '?')}: {models}")
        lines.append(f"- Analysts: {', '.join(analyst_names(s('analysts')))}; "
                     f"research debate rounds {s('max_debate_rounds', '?')}, "
                     f"risk debate rounds {s('max_risk_discuss_rounds', '?')}")
        vendors = {**(s("data_vendors") or {}), **(s("tool_vendors") or {})}
        if vendors:
            lines.append("- Data vendors: " + ", ".join(f"{k} {v}" for k, v in vendors.items()))
    if final_state.get("memory_note"):
        lines.append(f"- Memory log: {final_state['memory_note']}")
    return "\n".join(lines) + "\n\n"


# The report's sections in order: (heading, folder, [(agent, file, state path)]).
_SECTIONS = (
    ("I. Analyst Team Reports", "1_analysts", (
        ("Market Analyst", "market.md", ("market_report",)),
        ("Sentiment Analyst", "sentiment.md", ("sentiment_report",)),
        ("News Analyst", "news.md", ("news_report",)),
        ("Fundamentals Analyst", "fundamentals.md", ("fundamentals_report",)),
    )),
    ("II. Research Team Decision", "2_research", (
        ("Bull Researcher", "bull.md", ("investment_debate_state", "bull_history")),
        ("Bear Researcher", "bear.md", ("investment_debate_state", "bear_history")),
        ("Research Manager", "manager.md", ("investment_plan",)),
    )),
    ("III. Trading Team Plan", "3_trading", (
        ("Trader", "trader.md", ("trader_investment_plan",)),
    )),
    ("IV. Risk Management Team Decision", "4_risk", (
        ("Aggressive Analyst", "aggressive.md", ("risk_debate_state", "aggressive_history")),
        ("Conservative Analyst", "conservative.md", ("risk_debate_state", "conservative_history")),
        ("Neutral Analyst", "neutral.md", ("risk_debate_state", "neutral_history")),
    )),
    ("V. Portfolio Manager Decision", "5_portfolio", (
        ("Portfolio Manager", "decision.md", ("final_trade_decision",)),
    )),
)


def _report_parts(final_state: dict) -> list[tuple[str, str, list[tuple[str, str, str]]]]:
    """The sections with something to say: (heading, folder, [(agent, file, text)])."""
    parts = []
    for heading, folder, agents in _SECTIONS:
        written = []
        for agent, filename, path in agents:
            value = final_state
            for key in path:
                value = (value or {}).get(key)
            if value:
                written.append((agent, filename, value))
        if written:
            parts.append((heading, folder, written))
    return parts


def write_report_tree(final_state: dict, ticker: str, save_path, settings: dict | None = None,
                      html: bool = True) -> Path:
    """Save a completed run's reports to ``save_path``; return the complete-report path.

    ``settings`` (``TradingAgentsGraph.run_settings()``) adds what produced the run
    to the report's header. ``html`` also writes ``complete_report.html``, one
    self-contained page of the same report (#1419).
    Reusing a directory replaces the generated report files, removing sections
    absent from this run and disabled HTML. Other files and directories are kept.
    """
    save_path = Path(save_path)
    save_path.mkdir(parents=True, exist_ok=True)
    parts = _report_parts(final_state)
    quality_text = render_data_quality(final_state.get("data_quality") or [])
    if quality_text:
        # A vendor failure explains a thin section; put it before the reports
        # rather than leaving the reader to infer why one is missing.
        parts = [("Data Quality", "0_data_quality",
                  [("Run Data Quality", "quality.md", quality_text)])] + parts
    sections = []
    for heading, folder, written in parts:
        (save_path / folder).mkdir(exist_ok=True)
        for _agent, filename, text in written:
            (save_path / folder / filename).write_text(text, encoding="utf-8")
        content = "\n\n".join(f"### {agent}\n{text}" for agent, _filename, text in written)
        sections.append(f"## {heading}\n\n{content}")

    (save_path / "complete_report.md").write_text(
        _header(ticker, final_state, settings) + "\n\n".join(sections), encoding="utf-8"
    )
    if html:
        from tradingagents.report_html import render_report
        from tradingagents.report_visuals import build_chart_data_for_report

        chart_data = final_state.get("chart_data")
        if chart_data is None:
            try:
                chart_data = build_chart_data_for_report(ticker, final_state)
            except Exception:
                # A chart must never stop a report from being written.
                chart_data = {}
        (save_path / "complete_report.html").write_text(
            render_report(ticker, final_state, settings, parts, chart_data=chart_data),
            encoding="utf-8",
        )
    else:
        (save_path / "complete_report.html").unlink(missing_ok=True)

    # Reconcile only the filenames owned by this writer; never clear the tree,
    # since callers may keep notes or other artifacts alongside the reports.
    current_files = {
        (folder, filename)
        for _heading, folder, written in parts
        for _agent, filename, _text in written
    }
    for _heading, folder, agents in _SECTIONS:
        for _agent, filename, _path in agents:
            if (folder, filename) not in current_files:
                (save_path / folder / filename).unlink(missing_ok=True)
    if not quality_text:
        # A clean run must not inherit the previous run's warning.
        (save_path / "0_data_quality" / "quality.md").unlink(missing_ok=True)
    return save_path / "complete_report.md"


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def state_from_report_tree(report_dir) -> tuple[str, dict]:
    """Rebuild a minimal ``final_state`` from an already saved report tree.

    This is what makes an old run re-renderable without calling an LLM: the
    markdown files are the source, and the HTML page is rebuilt from them.
    """
    report_dir = Path(report_dir)
    complete = _read(report_dir / "complete_report.md")
    ticker_match = re.search(r"^#\s+Trading Analysis Report:\s*(\S+)", complete, re.MULTILINE)
    ticker = ticker_match.group(1) if ticker_match else report_dir.name.split("_")[0]
    date_match = re.search(r"^-\s+Analysis date:\s*(\d{4}-\d{2}-\d{2})", complete, re.MULTILINE)
    generated_match = re.search(r"^-\s+Generated:\s*(.+)$", complete, re.MULTILINE)
    memory_match = re.search(r"^-\s+Memory log:\s*(.+)$", complete, re.MULTILINE)
    state: dict = {
        "company_of_interest": ticker,
        "trade_date": date_match.group(1) if date_match else "",
        "generated_at": generated_match.group(1).strip() if generated_match else "",
        "memory_note": memory_match.group(1).strip() if memory_match else "",
        "market_report": _read(report_dir / "1_analysts" / "market.md"),
        "sentiment_report": _read(report_dir / "1_analysts" / "sentiment.md"),
        "news_report": _read(report_dir / "1_analysts" / "news.md"),
        "fundamentals_report": _read(report_dir / "1_analysts" / "fundamentals.md"),
        "investment_plan": _read(report_dir / "2_research" / "manager.md"),
        "trader_investment_plan": _read(report_dir / "3_trading" / "trader.md"),
        "final_trade_decision": _read(report_dir / "5_portfolio" / "decision.md"),
        "investment_debate_state": {
            "bull_history": _read(report_dir / "2_research" / "bull.md"),
            "bear_history": _read(report_dir / "2_research" / "bear.md"),
        },
        "risk_debate_state": {
            "aggressive_history": _read(report_dir / "4_risk" / "aggressive.md"),
            "conservative_history": _read(report_dir / "4_risk" / "conservative.md"),
            "neutral_history": _read(report_dir / "4_risk" / "neutral.md"),
        },
    }
    return ticker, state


def settings_from_report_header(complete: str) -> dict:
    """Recover the run details the header already records, for a rebuilt page."""
    settings: dict = {}
    match = re.search(r"^-\s+TradingAgents\s+([\d.]+):\s*(.+)$", complete, re.MULTILINE)
    if match:
        settings["version"] = match.group(1)
        models = match.group(2)
        provider = models.split(",")[0].strip()
        deep = re.search(r"\bdeep\s+([^,]+)", models)
        quick = re.search(r"\bquick\s+([^,]+)", models)
        settings["llm_provider"] = provider
        if deep:
            settings["deep_think_llm"] = deep.group(1).strip()
        if quick:
            settings["quick_think_llm"] = quick.group(1).strip()
    match = re.search(
        r"^-\s+Analysts:\s*(.+?);\s*research debate rounds\s*(\d+),\s*risk debate rounds\s*(\d+)",
        complete, re.MULTILINE,
    )
    if match:
        settings["analysts"] = [part.strip() for part in match.group(1).split(",")]
        settings["max_debate_rounds"] = int(match.group(2))
        settings["max_risk_discuss_rounds"] = int(match.group(3))
    match = re.search(r"^-\s+Data vendors:\s*(.+)$", complete, re.MULTILINE)
    if match:
        vendors, last_key = {}, None
        for part in match.group(1).split(", "):
            bits = part.strip().split(" ", 1)
            if len(bits) == 2:
                vendors[bits[0]] = bits[1]
                last_key = bits[0]
            elif last_key:  # a chain such as "sec_edgar,yfinance"
                vendors[last_key] += "," + part.strip()
        settings["data_vendors"] = vendors
    return settings


def rebuild_html(report_dir, settings: dict | None = None) -> Path:
    """Re-render ``complete_report.html`` from a saved report tree, no LLM calls."""
    from tradingagents.report_html import render_report
    from tradingagents.report_visuals import build_chart_data_for_report

    report_dir = Path(report_dir)
    ticker, state = state_from_report_tree(report_dir)
    if settings is None:
        settings = settings_from_report_header(_read(report_dir / "complete_report.md"))
    parts = _report_parts(state)
    quality_text = _read(report_dir / "0_data_quality" / "quality.md")
    if quality_text:
        parts = [("Data Quality", "0_data_quality",
                  [("Run Data Quality", "quality.md", quality_text)])] + parts
    chart_data = build_chart_data_for_report(ticker, state)
    page = render_report(ticker, state, settings, parts, chart_data=chart_data)
    target = report_dir / "complete_report.html"
    target.write_text(page, encoding="utf-8")
    return target
