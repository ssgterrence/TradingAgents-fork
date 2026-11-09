"""Company statements as they were filed, from SEC EDGAR.

Every other fundamentals vendor serves a period's current value and cuts the
statement at the fiscal period end. That is two claims a run should not make: a
period that has ended is not public until the company files, weeks later, and a
figure that was later restated is not what investors saw at the time.

EDGAR reports every fact with the date it was filed, so a run dated ``as_of_date``
serves exactly what was on file by then, restatements included at the vintage
that was current: Apple's 2008 total assets read 39.6B until the 2010 amendment
restated them to 36.2B.

Access needs no key or account, only a User-Agent identifying the caller, which
SEC requires and refuses requests without. US filers only: anything absent from
EDGAR's ticker map falls through to the next configured vendor.
"""

from __future__ import annotations

import json
import logging
import math
import os
import re
import time
import xml.etree.ElementTree as ET
from datetime import date, datetime
from pathlib import Path

import requests

from tradingagents import __version__
from tradingagents.dataflows.config import get_config
from tradingagents.dataflows.errors import NoMarketDataError, VendorUnavailableError
from tradingagents.dataflows.files import replace_file

logger = logging.getLogger(__name__)

_TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"
_FACTS_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
_SUBMISSIONS_URL = "https://data.sec.gov/submissions/CIK{cik}.json"
_ARCHIVE_INDEX_URL = "https://www.sec.gov/Archives/edgar/data/{cik}/{accession}/index.json"
_ARCHIVE_FILE_URL = "https://www.sec.gov/Archives/edgar/data/{cik}/{accession}/{name}"

# Segment revenue is a dimensional fact, which companyfacts does not carry.
# The latest 10-Q/10-K's XBRL instance does; read the segment axis there.
_SEGMENT_AXIS = "StatementBusinessSegmentsAxis"
_REVENUE_TAGS = (
    "RevenueFromContractWithCustomerExcludingAssessedTax",
    "RevenueFromContractWithCustomerIncludingAssessedTax",
    "Revenues",
    "SalesRevenueNet",
)
_XBRL_INSTANCE_MAX_BYTES = 20 * 1024 * 1024

# A filing history only changes when something new is filed, so one fetch per
# company per day serves every date a run asks about.
_CACHE_TTL_SECONDS = 24 * 60 * 60

# Line items, each with the tags filers use for it, best first. First match wins
# and values are never summed across tags: a company reporting revenue under two
# tags would otherwise be counted twice.
_STATEMENTS: dict[str, list[tuple[str, tuple[str, ...]]]] = {
    "balance_sheet": [
        ("Total Assets", ("Assets",)),
        ("Current Assets", ("AssetsCurrent",)),
        ("Cash and Equivalents", ("CashAndCashEquivalentsAtCarryingValue",)),
        ("Total Liabilities", ("Liabilities",)),
        ("Current Liabilities", ("LiabilitiesCurrent",)),
        ("Stockholders Equity", ("StockholdersEquity",
                                 "StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest")),
    ],
    "income_statement": [
        ("Revenue", ("RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues",
                     "SalesRevenueNet")),
        ("Cost of Revenue", ("CostOfRevenue", "CostOfGoodsAndServicesSold")),
        ("Gross Profit", ("GrossProfit",)),
        ("Operating Income", ("OperatingIncomeLoss",)),
        # The non-operating line and the tax line make the gap between operating
        # and net income readable from the filing, instead of reverse-engineering
        # it from an assumed tax rate (Alphabet's investment revaluations are a
        # large, two-way item there).
        ("Nonoperating Income (Expense)", ("NonoperatingIncomeExpense",
                                           "OtherNonoperatingIncomeExpense")),
        ("Pretax Income", ("IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest",
                           "IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments")),
        ("Income Tax Expense", ("IncomeTaxExpenseBenefit",)),
        ("Net Income", ("NetIncomeLoss",)),
        ("Diluted EPS", ("EarningsPerShareDiluted",)),
    ],
    "cashflow": [
        ("Operating Cash Flow", ("NetCashProvidedByUsedInOperatingActivities",
                                 "NetCashProvidedByUsedInOperatingActivitiesContinuingOperations")),
        ("Investing Cash Flow", ("NetCashProvidedByUsedInInvestingActivities",)),
        ("Financing Cash Flow", ("NetCashProvidedByUsedInFinancingActivities",)),
        ("Capital Expenditure", ("PaymentsToAcquirePropertyPlantAndEquipment",
                                 "PaymentsToAcquireProductiveAssets")),
    ],
}

# A statement's figures cover a span: a quarter is about 90 days, a year about
# 365. One filing reports both the quarter and the year to date under the same
# end date, so a match on the end date alone can report half a year as a quarter.
_SPANS = {"quarterly": (60, 115), "annual": (300, 400)}

# A 10-Q's cash flows are often filed only year to date. A quarterly table takes
# the quarter where filed, else the span to date, named in the column; it never
# subtracts one filing from another, which would give a figure no filing states.
_YEAR_TO_DATE = ((150, 200, 6), (240, 290, 9))

# A fiscal year is a period an annual report covers. A 10-Q balance has no span
# to reject, and some filers' 10-Qs report twelve-month totals that pass the span
# check, so either would read as a fiscal year. The value is still the latest
# filing of any form: a recast after a split or spin-off counts from its filing.
_ANNUAL_FORMS = ("10-K", "20-F", "40-F")


def _user_agent() -> str:
    """Who SEC sees. No account or key exists; callers identify themselves.

    www.sec.gov, which serves the ticker map, refuses a User-Agent carrying no
    contact address: a client name alone or with a project URL gets 403, one
    with an address gets 200. So the default carries a placeholder address and
    the package version. Set SEC_EDGAR_USER_AGENT to your own name and address
    so SEC can reach you about your traffic rather than the project.
    """
    configured = os.getenv("SEC_EDGAR_USER_AGENT", "").strip()
    return configured or f"TradingAgents/{__version__} (contact@example.com)"




def _fetch_json(url: str) -> dict:
    """Read a public EDGAR document, respecting SEC's identification rule."""
    try:
        response = requests.get(url, headers={"User-Agent": _user_agent()}, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        status = getattr(getattr(exc, "response", None), "status_code", None)
        # Every failure here is "this vendor cannot serve it now", so the router
        # moves on instead of seeing a transport exception it has no rule for.
        raise VendorUnavailableError(f"SEC EDGAR request failed ({status or type(exc).__name__})") from exc
    except ValueError as exc:
        raise VendorUnavailableError("SEC EDGAR returned an unreadable response") from exc


def _cached_json(url: str, name: str, refresh: bool = False) -> dict:
    path = Path(get_config()["data_cache_dir"]) / "sec_edgar" / name
    if not refresh and path.exists() and time.time() - path.stat().st_mtime < _CACHE_TTL_SECONDS:
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except ValueError:
            pass  # a truncated file is a miss, not a failure
    data = _fetch_json(url)
    path.parent.mkdir(parents=True, exist_ok=True)
    replace_file(path, lambda temp: Path(temp).write_text(json.dumps(data), encoding="utf-8"))
    return data


def _fetch_text(url: str) -> str:
    """Read a public EDGAR text/XML document, respecting SEC's identification rule."""
    try:
        with requests.get(
            url, headers={"User-Agent": _user_agent()}, timeout=30, stream=True,
        ) as response:
            response.raise_for_status()
            chunks = []
            total = 0
            for chunk in response.iter_content(chunk_size=65536):
                if not chunk:
                    continue
                total += len(chunk)
                if total > _XBRL_INSTANCE_MAX_BYTES:
                    raise VendorUnavailableError(
                        f"SEC EDGAR document exceeded {_XBRL_INSTANCE_MAX_BYTES} bytes; "
                        "refusing to parse"
                    )
                chunks.append(chunk)
            return b"".join(chunks).decode(response.encoding or "utf-8", errors="replace")
    except VendorUnavailableError:
        raise
    except requests.RequestException as exc:
        status = getattr(getattr(exc, "response", None), "status_code", None)
        raise VendorUnavailableError(f"SEC EDGAR request failed ({status or type(exc).__name__})") from exc


def _cached_text(url: str, name: str) -> str:
    path = Path(get_config()["data_cache_dir"]) / "sec_edgar" / name
    if path.exists() and time.time() - path.stat().st_mtime < _CACHE_TTL_SECONDS:
        try:
            return path.read_text(encoding="utf-8")
        except OSError:
            pass
    data = _fetch_text(url)
    path.parent.mkdir(parents=True, exist_ok=True)
    replace_file(path, lambda temp: Path(temp).write_text(data, encoding="utf-8"))
    return data


def _cik_in(table: dict, wanted: str) -> str | None:
    for entry in table.values():
        if entry.get("ticker", "").upper() == wanted:
            return f"{int(entry['cik_str']):010d}"
    return None


def cik_for(ticker: str) -> str | None:
    """The filer's CIK, or None when the ticker is not a US filer."""
    wanted = ticker.strip().upper()
    table = _cached_json(_TICKERS_URL, "company_tickers.json")
    found = _cik_in(table, wanted)
    if found is not None:
        return found
    # A stale or test-polluted cache must not make a US filer look non-US.
    # SEC's ticker map changes slowly, so one refresh per miss is enough.
    return _cik_in(_cached_json(_TICKERS_URL, "company_tickers.json", refresh=True), wanted)


def _span_index(fact: dict, spans: tuple[tuple[int, int], ...]) -> int | None:
    """Which of ``spans`` a duration fact covers (0 for an instant fact), or None."""
    if "start" not in fact:
        return 0
    days = (date.fromisoformat(fact["end"]) - date.fromisoformat(fact["start"])).days
    return next((i for i, (low, high) in enumerate(spans) if low <= days <= high), None)


def _as_of(facts: dict, tags: tuple[str, ...], as_of_date: str, spans: tuple[tuple[int, int], ...],
           forms: tuple[str, ...] = ()) -> tuple[dict, str]:
    """({(period end, span index): value}, unit) for the tags the filer reports, as known then.

    A period reported more than once takes its latest filing on or before the
    date, so an amendment counts from the day it was filed and not before. The
    unit comes from the filing: most lines are USD, earnings per share are
    USD/shares, and scaling those alike would print a real figure as zero. A
    duration fact (revenue, cash flow) must cover one of ``spans``; an instant
    fact (a balance) has no span and serves any.
    """
    values: dict[tuple[str, int], float] = {}
    chosen_unit = "USD"
    # Tags are tried in order and a period keeps the first one that reports it:
    # filers renamed lines over the years, so one tag covers only part of the
    # history. Values are never added across tags, which would double count.
    for tag in tags:
        for unit, unit_values in ((facts.get(tag) or {}).get("units", {})).items():
            latest: dict[tuple[str, int], dict] = {}
            covered: set[tuple[str, int]] = set()   # periods a filing of ``forms`` reports
            for fact in unit_values:
                index = _span_index(fact, spans)
                key = (fact["end"], index)
                if fact["filed"] > as_of_date or index is None or key in values:
                    continue
                if not forms or fact.get("form", "").startswith(forms):
                    covered.add(key)
                seen = latest.get(key)
                if seen is None or fact["filed"] >= seen["filed"]:
                    latest[key] = fact
            latest = {key: fact for key, fact in latest.items() if key in covered}
            if latest:
                chosen_unit = unit
                values.update({key: fact["val"] for key, fact in latest.items()})
    return dict(sorted(values.items())), chosen_unit


def _bare(name: str) -> str:
    """A Clark-notation or prefixed XML name without its namespace/prefix."""
    return name.rsplit("}", 1)[-1].rsplit(":", 1)[-1]


def _humanize_member(name: str) -> str:
    """``GoogleServicesMember`` -> ``Google Services`` for a readable table."""
    name = re.sub(r"Member$", "", name)
    return re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", name).strip() or name


def _latest_filing(
    cik: str,
    as_of_date: str,
    preferred: tuple[str, ...] = ("10-Q", "10-Q/A"),
) -> dict | None:
    """The newest 10-Q/10-K filed on or before ``as_of_date``, or None.

    ``preferred`` chooses the form that matches the statement's frequency (a
    quarterly income statement should read a 10-Q, an annual one a 10-K), so
    the segment table does not repeat a quarterly breakdown beside annual
    figures. When no preferred form is on file, the newest of either is used.
    """
    submissions = _cached_json(_SUBMISSIONS_URL.format(cik=cik), f"submissions-{cik}.json")
    recent = (submissions.get("filings") or {}).get("recent") or {}
    forms = recent.get("form") or []
    accessions = recent.get("accessionNumber") or []
    filed_dates = recent.get("filingDate") or []
    candidates = []
    for form, accession, filed in zip(forms, accessions, filed_dates, strict=False):
        if form in ("10-Q", "10-K", "10-Q/A", "10-K/A") and filed <= as_of_date:
            candidates.append({"form": form, "accession": accession, "filed": filed})
    if not candidates:
        return None
    return next((filing for filing in candidates if filing["form"] in preferred), candidates[0])


def _segment_instance_url(cik: str, accession: str) -> str | None:
    """The XBRL instance document of a filing, from its archive index."""
    accession_nodash = accession.replace("-", "")
    index = _cached_json(
        _ARCHIVE_INDEX_URL.format(cik=int(cik), accession=accession_nodash),
        f"index-{accession_nodash}.json",
    )
    # EDGAR's archive index has served both {"items": [...]} and
    # {"directory": {"item": [...]}} over time; accept either.
    items = index.get("items")
    if items is None:
        items = (index.get("directory") or {}).get("item") or []
    names = [str(item.get("name") or "") for item in items]
    candidates = [name for name in names if name.lower().endswith("_htm.xml")]
    if not candidates:
        skip = ("_cal", "_def", "_lab", "_pre", "_ref", "filingsummary")
        candidates = [
            name for name in names
            if name.lower().endswith(".xml") and not any(marker in name.lower() for marker in skip)
        ]
    if not candidates:
        return None
    return _ARCHIVE_FILE_URL.format(
        cik=int(cik), accession=accession_nodash, name=candidates[0],
    )


def _segment_revenue(cik: str, as_of_date: str, filing: dict) -> str:
    """Segment-axis revenue from the latest filing's XBRL instance, or an empty note.

    ``companyfacts`` carries only consolidated facts; the segment breakdown is a
    dimensional fact in the instance document. Only the latest two period ends
    are shown, so the table stays readable.
    """
    url = _segment_instance_url(cik, filing["accession"])
    if url is None:
        return ""
    xml = _cached_text(url, f"instance-{filing['accession'].replace('-', '')}.xml")
    root = ET.fromstring(xml)

    contexts: dict[str, tuple[str | None, str, str, int]] = {}
    for element in root.iter():
        if _bare(element.tag) != "context":
            continue
        context_id = element.get("id")
        period_start = period_end = None
        segment_members = []
        other_dimensions = []
        for child in element.iter():
            name = _bare(child.tag)
            if name == "startDate":
                period_start = (child.text or "").strip()
            elif name == "endDate":
                period_end = (child.text or "").strip()
            elif name == "explicitMember":
                dimension = _bare(child.get("dimension") or "")
                if dimension.endswith("Axis") and "Segment" in dimension:
                    segment_members.append(_bare((child.text or "").strip()))
                else:
                    other_dimensions.append(dimension)
        # Only the segment total: a context also sliced by product, geography,
        # or another axis is a sub-line (Google Search & other, YouTube, ...),
        # not the segment's revenue. Keeping only the single-dimension context
        # avoids reporting 63,350 as "Google Services" when the segment total
        # is 96,302.
        if (context_id and period_start and period_end
                and len(segment_members) == 1 and not other_dimensions):
            days = (date.fromisoformat(period_end) - date.fromisoformat(period_start)).days
            contexts[context_id] = (period_start, period_end, segment_members[0], days)
    if not contexts:
        return ""

    # A 10-Q may report the quarter and the year to date under one end date.
    # Keep the shortest span for a period/segment, so a quarter is not replaced
    # by a nine-month total.
    rows: dict[tuple[str, str], tuple[float, int]] = {}
    for tag in _REVENUE_TAGS:
        for element in root.iter():
            if _bare(element.tag) != tag:
                continue
            context = contexts.get(element.get("contextRef"))
            if context is None:
                continue
            try:
                value = float(element.text)
            except (TypeError, ValueError):
                continue
            key = (context[1], context[2])
            if key not in rows or context[3] < rows[key][1]:
                rows[key] = (value, context[3])
    if not rows:
        return ""

    periods = sorted({end for end, _member in rows}, reverse=True)[:2]
    lines = [
        f"# Segment revenue as filed (latest 10-Q/10-K on or before {as_of_date})",
        f"# Source: {filing['form']} filed {filing['filed']} "
        f"(accession {filing['accession']})",
        "# Segment names are the filer's XBRL segment-axis members.",
        "Period end,Segment,Revenue (USD millions)",
    ]
    for end in periods:
        for period_end, member in sorted(rows):
            if period_end == end:
                lines.append(
                    f"{end},{_humanize_member(member)},{_millions(rows[(period_end, member)][0])}"
                )
    return "\n".join(lines) + "\n"


def _statement(kind: str, ticker: str, freq: str, as_of_date: str, title: str) -> str:
    as_of_date = as_of_date or datetime.now().strftime("%Y-%m-%d")
    cik = cik_for(ticker)
    if cik is None:
        raise NoMarketDataError(ticker, ticker, "not a US SEC filer")

    facts = _cached_json(_FACTS_URL.format(cik=cik), f"CIK{cik}.json")
    us_gaap = (facts.get("facts") or {}).get("us-gaap")
    if not us_gaap:
        raise NoMarketDataError(ticker, ticker, "US filer with no us-gaap facts")

    quarterly = freq.lower() == "quarterly"
    if quarterly:
        spans = (_SPANS["quarterly"], *((low, high) for low, high, _ in _YEAR_TO_DATE))
        names = ["", *(f" ({months} months)" for _, _, months in _YEAR_TO_DATE)]
    else:
        spans, names = (_SPANS["annual"],), [""]
    forms = () if quarterly else _ANNUAL_FORMS
    lines = {label: _as_of(us_gaap, tags, as_of_date, spans, forms) for label, tags in _STATEMENTS[kind]}
    # Each row takes the shortest span it reports for a period, and a column
    # holds one span of one period, so a row filed only to date keeps its figure
    # beside a row filed by quarter.
    chosen = {label: {} for label in lines}
    for label, (values, _) in lines.items():
        for end, index in values:
            chosen[label][end] = min(index, chosen[label].get(end, index))
    periods = sorted({(end, index) for spans_of in chosen.values() for end, index in spans_of.items()})
    if not periods:
        raise NoMarketDataError(ticker, ticker, f"no {freq} {title.lower()} filed by {as_of_date}")
    tagged = {label: line for label, line in lines.items() if line[0]}
    untagged = [label for label in lines if label not in tagged]
    # Say what this vendor does not serve, so a thin section is not mistaken for
    # a gap the model should fill by estimation. Segment revenue lives in a
    # filing's dimensional facts, and non-GAAP reconciliations in 8-K exhibits;
    # neither is part of the consolidated companyfacts feed used here.
    coverage = ""
    if kind == "income_statement":
        coverage = (
            "# Coverage: consolidated figures from companyfacts; segment revenue, "
            "when filed, follows the table; non-GAAP reconciliations are not served "
            "(the GAAP non-operating and tax lines make the operating-to-net bridge "
            "explicit).\n"
        )
    elif kind == "cashflow":
        coverage = (
            "# Free cash flow is not a filed line: compute Operating Cash Flow minus "
            "Capital Expenditure over the same period, and do not compare it to a "
            "vendor's freeCashflow field without checking that vendor's definition.\n"
        )
    header = (
        f"# {title} for {ticker.upper()} ({freq}), USD in millions unless the column says otherwise\n"
        f"# SEC EDGAR facts filed on or before {as_of_date}, at the values filed then\n"
        + coverage
        + (f"# Not tagged by this filer: {', '.join(untagged)}\n" if untagged else "")
        + "\n"
    )
    # One row per period, so every figure sits beside its own date: across a
    # filer's whole history a row per line item ran to dozens of columns and was
    # read a column off (#1517).
    rows = [",".join(["Period"] + [label if unit == "USD" else f"{label} ({unit})"
                                   for label, (_, unit) in tagged.items()])]
    for end, index in periods:
        cells = []
        for label, (values, unit) in tagged.items():
            value = values.get((end, index)) if chosen[label].get(end) == index else None
            cells.append("" if value is None else _millions(value) if unit == "USD" else f"{value:.2f}")
        rows.append(",".join([end + names[index]] + cells))
    derived = _derived_ttm_cashflow(us_gaap, as_of_date, quarterly) if kind == "cashflow" else ""
    segments = ""
    if kind == "income_statement":
        try:
            preferred = (("10-Q", "10-Q/A") if quarterly else ("10-K", "10-K/A"))
            filing = _latest_filing(cik, as_of_date, preferred)
            if filing:
                segments = _segment_revenue(cik, as_of_date, filing)
        except (VendorUnavailableError, ET.ParseError, ValueError) as exc:
            # The consolidated statement is already complete; a segment
            # enrichment failure is a note, not a reason to lose the report.
            logger.warning("Segment revenue unavailable for %s: %s", ticker, exc)
            segments = (
                f"# Segment revenue: not available this run ({type(exc).__name__}); "
                "the consolidated figures above are unaffected.\n"
            )
    return header + "\n".join(rows) + "\n" + derived + segments


def _ttm_for(values: dict, annual_values: dict) -> tuple[str, float] | None:
    """A trailing-twelve-month figure from filed annual and year-to-date values.

    A 10-Q cash flow is often filed only year to date, so TTM is the last fiscal
    year plus this year to date minus the same span a year earlier. That is a
    derived figure, not one any filing states; the caller labels it as such.
    Discrete quarters are summed only when four are actually filed.
    """
    if not values:
        return None
    end, index = max(values)
    if index == 0:
        quarters = sorted({period for period, span in values if span == 0}, reverse=True)
        if len(quarters) < 4:
            return None
        picked = quarters[:4]
        if (date.fromisoformat(picked[0]) - date.fromisoformat(picked[3])).days > 400:
            return None
        return picked[0], sum(values[(period, 0)] for period in picked)

    end_date = date.fromisoformat(end)
    try:
        target = end_date.replace(year=end_date.year - 1)
    except ValueError:  # 29 February in a non-leap prior year
        target = date(end_date.year - 1, 12, 31)
    # A 52/53-week filer's prior-year span can end a few days away from the
    # calendar anniversary. Match the nearest same-span period within 10 days;
    # a wider gap is a different period and must not be subtracted.
    prior_key = min(
        (key for key in values if key[1] == index),
        key=lambda key: abs((date.fromisoformat(key[0]) - target).days),
        default=None,
    )
    if prior_key is None or abs((date.fromisoformat(prior_key[0]) - target).days) > 10:
        return None
    annual_period = max((period for period in annual_values if period[0] < end), default=None)
    if annual_period is None:
        return None
    return end, annual_values[annual_period] + values[(end, index)] - values[prior_key]


def _derived_ttm_cashflow(us_gaap: dict, as_of_date: str, quarterly: bool) -> str:
    """A statement-derived TTM cash flow note, or an empty string."""
    if not quarterly:
        return ""
    spans = (_SPANS["quarterly"], *((low, high) for low, high, _ in _YEAR_TO_DATE))
    annual_spans = (_SPANS["annual"],)
    labels = {label: _as_of(us_gaap, tags, as_of_date, spans) for label, tags in _STATEMENTS["cashflow"]}
    annual = {
        label: _as_of(us_gaap, tags, as_of_date, annual_spans, _ANNUAL_FORMS)[0]
        for label, tags in _STATEMENTS["cashflow"]
    }
    ocf = _ttm_for(labels["Operating Cash Flow"][0], annual["Operating Cash Flow"])
    capex = _ttm_for(labels["Capital Expenditure"][0], annual["Capital Expenditure"])
    if ocf is None or capex is None or ocf[0] != capex[0]:
        return ""
    end = ocf[0]
    return (
        f"# Derived (not filed): TTM cash flow as of {end}\n"
        f"# Operating Cash Flow TTM: {_millions(ocf[1])}\n"
        f"# Capital Expenditure TTM: {_millions(capex[1])}\n"
        f"# Free Cash Flow TTM (Operating Cash Flow - Capital Expenditure): {_millions(ocf[1] - capex[1])}\n"
        f"# Free cash flow is a derived metric, not a figure any filing states; state\n"
        f"# its definition and window when comparing it with a vendor's figure.\n"
    )


def _millions(value: float) -> str:
    """USD in millions; under a million, three significant digits, so it is not printed as 0.

    Plain numbers: a thousands separator would split the CSV field.
    """
    millions = value / 1e6
    if millions == 0 or abs(millions) >= 1:
        return f"{millions:.0f}"
    return f"{millions:.{2 - math.floor(math.log10(abs(millions)))}f}"


def get_balance_sheet(ticker: str, freq: str = "quarterly", as_of_date: str | None = None) -> str:
    """Balance sheet as filed on or before ``as_of_date``."""
    return _statement("balance_sheet", ticker, freq, as_of_date, "Balance Sheet")


def get_income_statement(ticker: str, freq: str = "quarterly", as_of_date: str | None = None) -> str:
    """Income statement as filed on or before ``as_of_date``.

    A fourth quarter is never derived: filers report it only inside the annual
    figure, and subtracting three separately filed quarters would invent a number
    with no filing date behind it.
    """
    return _statement("income_statement", ticker, freq, as_of_date, "Income Statement")


def get_cashflow(ticker: str, freq: str = "quarterly", as_of_date: str | None = None) -> str:
    """Cash flow statement as filed on or before ``as_of_date``."""
    return _statement("cashflow", ticker, freq, as_of_date, "Cash Flow Statement")
