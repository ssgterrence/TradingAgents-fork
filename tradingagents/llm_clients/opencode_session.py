"""Headers the OpenCode Go router requires on every LLM request.

Requests routed through opencode.ai (e.g. ``TRADINGAGENTS_LLM_BACKEND_URL=
https://opencode.ai/zen/go/v1``) are rejected with ``400 MissingSessionID``
unless each conversation sends a stable session ID in ``x-opencode-session``
(https://opencode.ai/docs/go/#where-can-i-use-it). Go also asks clients to
identify themselves with their own user agent instead of the SDK's generic one.
"""

import os
import uuid
from urllib.parse import urlparse

from tradingagents import __version__

# Pins the session ID (e.g. to keep prompt caching warm across runs). When
# unset, one ID is generated per process; the run's quick and deep tier LLMs
# are both built at graph setup (trading_graph.py), so the ID is stable for
# every conversation in a run — which is what Go routes and caches on.
SESSION_ID_ENV = "TRADINGAGENTS_LLM_SESSION_ID"

_session_id: str | None = None


def is_opencode_endpoint(base_url: str | None) -> bool:
    """True when ``base_url`` points at opencode.ai or one of its subdomains.

    Scheme-less URLs are tolerated (``opencode.ai/zen/go/v1``), matching
    ``openai_client._is_native_openai_base_url``. A suffix impostor such as
    ``notopencode.ai`` is not a match.
    """
    if not base_url:
        return False
    if "://" not in base_url:
        base_url = "https://" + base_url
    host = urlparse(base_url).hostname or ""
    return host == "opencode.ai" or host.endswith(".opencode.ai")


def session_id() -> str:
    """The stable session ID sent in ``x-opencode-session``."""
    global _session_id
    pinned = os.environ.get(SESSION_ID_ENV)
    if pinned:
        return pinned
    if _session_id is None:
        _session_id = uuid.uuid4().hex
    return _session_id


def request_headers(base_url: str | None) -> dict[str, str] | None:
    """Extra request headers for an OpenCode endpoint, else ``None``."""
    if not is_opencode_endpoint(base_url):
        return None
    return {
        "x-opencode-session": session_id(),
        "User-Agent": f"tradingagents/{__version__}",
    }
