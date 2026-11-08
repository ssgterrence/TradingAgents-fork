"""Per-run record of data-vendor calls, so a thin report can say why.

Every data tool goes through :func:`tradingagents.dataflows.router.route_to_vendor`,
which is the one place that knows whether a call was served, retried on another
vendor, or failed. Without a record, a section that is missing data looks the
same as a section where the vendor simply had nothing, and a reader is left to
guess. This ledger keeps the facts in one place.

The analysts run in parallel threads, so appends are guarded by a lock. A run
resets the ledger before the graph starts and copies the snapshot into its
state; the report writer turns it into a Data Quality note.
"""

from __future__ import annotations

import threading
from collections import Counter

_lock = threading.Lock()
_entries: list[dict] = []


def reset() -> None:
    """Forget the previous run's calls."""
    with _lock:
        _entries.clear()


def record(
    method: str,
    category: str,
    status: str,
    chain: list[str],
    served_by: str | None = None,
    failures: list[tuple[str, str]] | None = None,
) -> None:
    """Keep one call's outcome: ``ok``, ``fallback`` (served after a failure), or ``failed``."""
    entry = {
        "method": method,
        "category": category,
        "status": status,
        "chain": list(chain),
        "served_by": served_by,
        "failures": [{"vendor": vendor, "error": error} for vendor, error in (failures or [])],
    }
    with _lock:
        _entries.append(entry)


def snapshot() -> list[dict]:
    """A copy of the current run's calls."""
    with _lock:
        return [dict(entry) for entry in _entries]


def render_markdown(entries: list[dict]) -> str:
    """A Data Quality section for the calls that did not simply succeed.

    Returns an empty string when everything succeeded, so an ordinary report is
    not given a table that says nothing. A failure here describes the vendor,
    not the instrument: the note says so, because a missing row must never be
    read as "no news" or "the company has no data".
    """
    notable = [entry for entry in entries if entry.get("status") != "ok"]
    if not notable:
        return ""

    by_method: dict[str, list[dict]] = {}
    for entry in notable:
        by_method.setdefault(entry["method"], []).append(entry)

    rows = []
    for method, calls in sorted(by_method.items()):
        served = sorted({c["served_by"] for c in calls if c.get("served_by")})
        failure_counts: Counter[tuple[str, str]] = Counter(
            (failure["vendor"], failure["error"])
            for call in calls
            for failure in call.get("failures", [])
        )
        failures_text = ", ".join(
            f"{vendor} ({error})" + (f" x{count}" if count > 1 else "")
            for (vendor, error), count in failure_counts.items()
        ) or "—"
        rows.append(f"| {method} | {len(calls)} | {', '.join(served) or '—'} | {failures_text} |")

    return (
        "Data Quality: calls that failed or needed a fallback. A failure here is a "
        "vendor failure, not evidence about the instrument; do not read a missing "
        "row as \"no news\" or \"no data exists\".\n\n"
        "| Tool | Calls | Served by | Failed attempts |\n"
        "| --- | ---: | --- | --- |\n"
        + "\n".join(rows)
    )
