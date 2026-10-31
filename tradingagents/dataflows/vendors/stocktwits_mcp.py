"""StockTwits through its remote MCP server, instead of the blocked public REST feed.

Why this exists
---------------
``api.stocktwits.com/api/2/streams/symbol/{ticker}.json`` is fronted by
Cloudflare and answers ordinary clients with ``403`` (a "Just a moment..."
challenge). StockTwits' supported path is its MCP server at
``https://mcp.stocktwits.com/mcp``: OAuth 2.0 (dynamic client registration +
PKCE) followed by JSON-RPC over the MCP Streamable HTTP transport.

This module is deliberately stdlib-only (``urllib``), so it adds no dependency
and can be tested without the rest of the data stack. It is used by
``tradingagents.dataflows.vendors.stocktwits`` when a token is configured.

Authentication
--------------
Run ``tradingagents stocktwits-login`` once. Tokens are stored in
``~/.tradingagents/stocktwits-auth.json`` (mode 0600) and refreshed
automatically. For CI, set ``STOCKTWITS_MCP_TOKEN`` to an access token instead;
it is used as-is and never refreshed.

Environment
-----------
``STOCKTWITS_MCP_URL``          MCP endpoint (default ``https://mcp.stocktwits.com/mcp``)
``STOCKTWITS_MCP_TOKEN``        bearer access token, overrides the token file
``STOCKTWITS_AUTH_PATH``        token file path
``STOCKTWITS_MCP_DISABLE``      set to any value to force the legacy REST path
``STOCKTWITS_MCP_USER_AGENT``   override the User-Agent sent to Cloudflare
"""

from __future__ import annotations

import base64
import contextlib
import hashlib
import json
import logging
import os
import secrets
import threading
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import parse_qs, urlencode, urlparse
from urllib.request import Request, urlopen

logger = logging.getLogger(__name__)

DEFAULT_MCP_URL = "https://mcp.stocktwits.com/mcp"
_DEFAULT_SCOPE = "read watch_lists"
_PROTOCOL_VERSION = "2025-06-18"
_TIMEOUT = 20.0
_MAX_MESSAGES = 50

# Cloudflare's WAF rejects urllib's default ``Python-urllib/x.y`` signature with
# error 1010 ("browser signature banned"). A browser-like User-Agent is enough to
# pass; the MCP server itself authenticates with the bearer token.
_DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36"
)


class StockTwitsMCPError(Exception):
    """The MCP server could not answer."""


class StockTwitsAuthRequired(StockTwitsMCPError):
    """No usable token: run ``tradingagents stocktwits-login``."""


# --------------------------------------------------------------------------- #
# Token storage
# --------------------------------------------------------------------------- #

def _auth_path() -> Path:
    configured = os.getenv("STOCKTWITS_AUTH_PATH")
    if configured:
        return Path(configured).expanduser()
    return Path.home() / ".tradingagents" / "stocktwits-auth.json"


def load_token() -> dict | None:
    """The stored token, or None when absent/unreadable."""
    try:
        data = json.loads(_auth_path().read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return data if isinstance(data, dict) and data.get("access_token") else None


def save_token(token: dict) -> None:
    """Write the token with owner-only permissions."""
    path = _auth_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(token, indent=2), encoding="utf-8")
    with contextlib.suppress(OSError):
        os.chmod(tmp, 0o600)
    tmp.replace(path)


def logout() -> bool:
    """Delete the stored token; True when one was removed."""
    path = _auth_path()
    try:
        path.unlink()
        return True
    except FileNotFoundError:
        return False
    except OSError as exc:
        raise StockTwitsMCPError(f"could not remove {path}: {exc}") from exc


def available() -> bool:
    """Whether the MCP path is configured and enabled."""
    if os.getenv("STOCKTWITS_MCP_DISABLE"):
        return False
    if os.getenv("STOCKTWITS_MCP_TOKEN"):
        return True
    return load_token() is not None


def status() -> dict:
    """A small, secret-free description for the CLI status command."""
    env_token = bool(os.getenv("STOCKTWITS_MCP_TOKEN"))
    token = load_token()
    expires_at = (token or {}).get("expires_at")
    return {
        "source": "env" if env_token else ("file" if token else None),
        "path": str(_auth_path()),
        "expires_at": expires_at,
        "expired": bool(expires_at and expires_at <= _now_ms()),
    }


def _now_ms() -> int:
    return int(time.time() * 1000)


# --------------------------------------------------------------------------- #
# HTTP
# --------------------------------------------------------------------------- #

def _user_agent() -> str:
    return os.getenv("STOCKTWITS_MCP_USER_AGENT") or _DEFAULT_USER_AGENT


def _header(headers: dict, name: str) -> str | None:
    """Case-insensitive header lookup (dict() loses Message's own lookup)."""
    wanted = name.lower()
    for key, value in headers.items():
        if key.lower() == wanted:
            return value
    return None


def _request(
    url: str,
    method: str = "GET",
    body: bytes | None = None,
    headers: dict | None = None,
    timeout: float = _TIMEOUT,
) -> tuple[int, dict, bytes]:
    """One HTTP request; errors are returned, not raised, so callers can report them."""
    merged = {"User-Agent": _user_agent(), "Accept": "application/json"}
    merged.update(headers or {})
    req = Request(url, data=body, method=method, headers=merged)
    try:
        with urlopen(req, timeout=timeout) as resp:
            return resp.status, dict(resp.headers), resp.read()
    except HTTPError as exc:
        return exc.code, dict(exc.headers or {}), exc.read()
    except OSError as exc:  # URLError, TimeoutError, connection resets
        raise StockTwitsMCPError(f"request to {url} failed: {exc}") from exc


def _post_form(url: str, fields: dict, timeout: float = _TIMEOUT) -> dict:
    status, _, raw = _request(
        url,
        "POST",
        urlencode(fields).encode(),
        {"Content-Type": "application/x-www-form-urlencoded", "Accept": "application/json"},
        timeout,
    )
    if status not in (200, 201):
        raise StockTwitsMCPError(f"{url} returned HTTP {status}: {raw[:300].decode(errors='replace')}")
    try:
        return json.loads(raw)
    except ValueError as exc:
        raise StockTwitsMCPError(f"{url} returned an unreadable response") from exc


def _get_json(url: str, timeout: float = _TIMEOUT) -> dict:
    status, _, raw = _request(url, "GET", timeout=timeout)
    if status != 200:
        raise StockTwitsMCPError(f"{url} returned HTTP {status}")
    try:
        return json.loads(raw)
    except ValueError as exc:
        raise StockTwitsMCPError(f"{url} returned an unreadable response") from exc


# --------------------------------------------------------------------------- #
# Token refresh
# --------------------------------------------------------------------------- #

_refresh_lock = threading.Lock()


def _refresh(token: dict) -> str:
    """Refresh an expired token, persisting the rotated pair."""
    endpoint = token.get("token_endpoint")
    refresh_token = token.get("refresh_token")
    client_id = token.get("client_id")
    if not (endpoint and refresh_token and client_id):
        raise StockTwitsAuthRequired(
            "the StockTwits MCP token has expired and cannot be refreshed; "
            "run `tradingagents stocktwits-login` again"
        )
    with _refresh_lock:
        # Another thread may have refreshed while this one waited.
        current = load_token()
        if current and current.get("access_token") != token.get("access_token"):
            if current.get("expires_at", 0) > _now_ms() + 60_000:
                return current["access_token"]
            token = current
            endpoint = token.get("token_endpoint")
            refresh_token = token.get("refresh_token")
            client_id = token.get("client_id")
        data = _post_form(endpoint, {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": client_id,
            "resource": token.get("resource") or _mcp_url(),
        })
        updated = {
            **token,
            "access_token": data["access_token"],
            "refresh_token": data.get("refresh_token") or refresh_token,
            "expires_at": _now_ms() + int(data.get("expires_in", 3600)) * 1000,
            "scope": data.get("scope") or token.get("scope") or _DEFAULT_SCOPE,
            "saved_at": _now_ms(),
        }
        save_token(updated)
        return updated["access_token"]


def _access_token() -> str:
    """A valid bearer token from the environment or the token file."""
    env_token = os.getenv("STOCKTWITS_MCP_TOKEN")
    if env_token:
        return env_token
    token = load_token()
    if token is None:
        raise StockTwitsAuthRequired(
            "no StockTwits MCP token; run `tradingagents stocktwits-login` "
            "or set STOCKTWITS_MCP_TOKEN"
        )
    if token.get("expires_at", 0) > _now_ms() + 60_000:
        return token["access_token"]
    return _refresh(token)


# --------------------------------------------------------------------------- #
# MCP transport
# --------------------------------------------------------------------------- #

def _mcp_url() -> str:
    return os.getenv("STOCKTWITS_MCP_URL") or DEFAULT_MCP_URL


def _sse_payload(raw: str, want_id: int | None = None) -> dict:
    """The JSON-RPC object in an SSE or plain-JSON response.

    Streamable HTTP may answer with ``text/event-stream``; one event carries the
    result and others may be logging notifications. A plain JSON body is also
    accepted, because the transport may negotiate either.
    """
    objects: list[dict] = []
    for block in raw.split("\n\n"):
        data = [line[5:].strip() for line in block.splitlines() if line.startswith("data:")]
        if not data:
            continue
        try:
            objects.append(json.loads("\n".join(data)))
        except ValueError:
            continue
    if not objects:
        try:
            objects = [json.loads(raw)]
        except ValueError as exc:
            raise StockTwitsMCPError("MCP response was not JSON or SSE") from exc
    if want_id is not None:
        for obj in objects:
            if obj.get("id") == want_id:
                return obj
    return objects[-1]


class _MCPClient:
    """One MCP session: initialize once, then ``tools/call``."""

    def __init__(self, url: str, token: str, timeout: float):
        self.url = url
        self.token = token
        self.timeout = timeout
        self.session: str | None = None
        self._initialized = False
        self._next_id = 0
        self._lock = threading.Lock()

    def _id(self) -> int:
        self._next_id += 1
        return self._next_id

    def _post(self, payload: dict) -> tuple[int, str]:
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        }
        if self.session:
            headers["Mcp-Session-Id"] = self.session
        status, response_headers, raw = _request(
            self.url, "POST", json.dumps(payload).encode(), headers, self.timeout
        )
        session = _header(response_headers, "Mcp-Session-Id")
        if session:
            self.session = session
        return status, raw.decode(errors="replace")

    def initialize(self) -> None:
        status, raw = self._post({
            "jsonrpc": "2.0",
            "id": self._id(),
            "method": "initialize",
            "params": {
                "protocolVersion": _PROTOCOL_VERSION,
                "capabilities": {},
                "clientInfo": {"name": "TradingAgents", "version": "1.0"},
            },
        })
        if status != 200:
            raise StockTwitsMCPError(f"MCP initialize returned HTTP {status}: {raw[:200]}")
        self._post({"jsonrpc": "2.0", "method": "notifications/initialized"})
        self._initialized = True

    def call_tool(self, name: str, arguments: dict) -> dict:
        with self._lock:
            if not self._initialized:
                self.initialize()
            for attempt in (1, 2):
                request_id = self._id()
                status, raw = self._post({
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "method": "tools/call",
                    "params": {"name": name, "arguments": arguments},
                })
                # A restarted server forgets the session id; start a new one once.
                if status in (400, 404) and self.session and attempt == 1:
                    self.session = None
                    self._initialized = False
                    self.initialize()
                    continue
                break
        if status != 200:
            raise StockTwitsMCPError(f"MCP tools/call returned HTTP {status}: {raw[:200]}")
        payload = _sse_payload(raw, want_id=request_id)
        if payload.get("error"):
            message = payload["error"].get("message") if isinstance(payload["error"], dict) else payload["error"]
            raise StockTwitsMCPError(f"MCP error: {message}")
        result = payload.get("result") or {}
        if result.get("isError"):
            raise StockTwitsMCPError(f"MCP tool {name} reported an error")
        return result


_client: _MCPClient | None = None
_client_lock = threading.Lock()


def _client_for(token: str, timeout: float) -> _MCPClient:
    global _client
    with _client_lock:
        if _client is None or _client.token != token or _client.timeout != timeout:
            _client = _MCPClient(_mcp_url(), token, timeout)
        return _client


def reset_client() -> None:
    """Drop the cached session (tests, or after a token change)."""
    global _client
    with _client_lock:
        _client = None


def _tool_json(result: dict) -> dict:
    """Parse the JSON document these StockTwits tools put in ``content[].text``."""
    for item in result.get("content") or []:
        if item.get("type") == "text":
            text = item.get("text") or ""
            try:
                return json.loads(text)
            except ValueError:
                continue
    raise StockTwitsMCPError("MCP tool returned no JSON content")


def _normalize_message(message: dict) -> dict:
    """Give MCP messages the shape the existing formatter expects.

    The REST feed nested a user label at ``entities.sentiment.basic``; MCP puts a
    top-level ``sentiment`` string. Normalizing here keeps the formatter, window
    filtering and Jev screening unchanged.
    """
    normalized = dict(message)
    sentiment = message.get("sentiment")
    entities = message.get("entities")
    if not isinstance(entities, dict):
        entities = {}
    if sentiment and not (entities.get("sentiment") or {}).get("basic"):
        entities = {**entities, "sentiment": {"basic": sentiment}}
    normalized["entities"] = entities
    normalized.setdefault("body", "")
    normalized.setdefault("created_at", "")
    normalized.setdefault("user", {})
    return normalized


def fetch_messages(symbol: str, limit: int = 30, timeout: float | None = None) -> list[dict]:
    """Recent messages about ``symbol`` via MCP, normalized for the formatter.

    ``symbol`` is the StockTwits symbol (``GOOGL``, ``BTC.X``). Raises
    ``StockTwitsAuthRequired`` when no token is configured and
    ``StockTwitsMCPError`` when the server cannot answer.
    """
    token = _access_token()
    client = _client_for(token, timeout or _TIMEOUT)
    result = client.call_tool(
        "get_symbol_messages",
        {"symbol": symbol, "limit": max(1, min(int(limit), _MAX_MESSAGES))},
    )
    payload = _tool_json(result)
    messages = payload.get("messages") if isinstance(payload, dict) else None
    return [_normalize_message(m) for m in (messages or []) if isinstance(m, dict)]


# --------------------------------------------------------------------------- #
# OAuth login
# --------------------------------------------------------------------------- #

def _discover(url: str, fallback: dict) -> dict:
    try:
        return {**fallback, **_get_json(url)}
    except StockTwitsMCPError as exc:
        logger.info("OAuth discovery at %s failed (%s); using defaults", url, exc)
        return fallback


def _pkce() -> tuple[str, str]:
    verifier = secrets.token_urlsafe(64)[:96]
    digest = hashlib.sha256(verifier.encode()).digest()
    challenge = base64.urlsafe_b64encode(digest).rstrip(b"=").decode()
    return verifier, challenge


class _CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):  # noqa: N802 - BaseHTTPRequestHandler API
        parsed = urlparse(self.path)
        # Browsers may ask for /favicon.ico before or after the redirect; only
        # the callback path carries the authorization code.
        if parsed.path != "/callback":
            self.send_response(404)
            self.end_headers()
            return
        self.server.result = parse_qs(parsed.query)  # type: ignore[attr-defined]
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(
            b"<html><body><h3>TradingAgents is signed in to StockTwits.</h3>"
            b"<p>You can close this window and return to the terminal.</p></body></html>"
        )

    def log_message(self, *_args):
        pass


def login(
    manual: bool = False,
    timeout: int = 180,
    open_browser: bool = True,
    echo=print,
) -> dict:
    """Sign in with OAuth (dynamic registration + PKCE) and store the token.

    ``manual`` skips the local callback server: the browser shows a connection
    error after redirecting, and the user pastes the full URL from its address
    bar. Use it over SSH, in Docker, or when the browser runs elsewhere.
    """
    mcp_url = _mcp_url()
    parsed = urlparse(mcp_url)
    well_known = f"{parsed.scheme}://{parsed.netloc}/.well-known"
    resource = _discover(f"{well_known}/oauth-protected-resource", {
        "resource": mcp_url,
        "authorization_servers": [f"{parsed.scheme}://{parsed.netloc}"],
        "scopes_supported": _DEFAULT_SCOPE.split(),
    })
    server_url = (resource.get("authorization_servers") or ["https://mcp.stocktwits.com"])[0]
    metadata = _discover(f"{server_url.rstrip('/')}/.well-known/oauth-authorization-server", {
        "issuer": server_url,
        "registration_endpoint": f"{server_url.rstrip('/')}/register",
        "authorization_endpoint": f"{server_url.rstrip('/')}/authorize",
        "token_endpoint": f"{server_url.rstrip('/')}/token",
        "scopes_supported": _DEFAULT_SCOPE.split(),
    })
    scope = " ".join(resource.get("scopes_supported") or _DEFAULT_SCOPE.split())

    server = None
    if manual:
        redirect_uri = "http://127.0.0.1:8765/callback"
    else:
        server = HTTPServer(("127.0.0.1", 0), _CallbackHandler)
        server.timeout = max(30, timeout)
        redirect_uri = f"http://127.0.0.1:{server.server_address[1]}/callback"

    registration = _post_json(metadata["registration_endpoint"], {
        "client_name": "TradingAgents",
        "redirect_uris": [redirect_uri],
        "grant_types": ["authorization_code", "refresh_token"],
        "response_types": ["code"],
        "token_endpoint_auth_method": "none",
        "scope": scope,
    })
    client_id = registration.get("client_id")
    if not client_id:
        raise StockTwitsMCPError("OAuth registration returned no client_id")

    verifier, challenge = _pkce()
    state = secrets.token_urlsafe(24)
    authorize_url = metadata["authorization_endpoint"] + "?" + urlencode({
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": scope,
        "state": state,
        "code_challenge": challenge,
        "code_challenge_method": "S256",
        "resource": mcp_url,
    })

    echo("Open this address to sign in to StockTwits:")
    echo(authorize_url)
    if open_browser:
        with contextlib.suppress(Exception):  # a headless box gets the printed URL
            webbrowser.open(authorize_url)

    code = None
    if manual:
        pasted = input("Paste the full redirect URL (or just the code): ").strip()
        if "code=" in pasted:
            query = parse_qs(urlparse(pasted).query)
            if query.get("state", [None])[0] not in (None, state):
                raise StockTwitsMCPError("authorization state did not match")
            code = query.get("code", [None])[0]
        else:
            code = pasted or None
    else:
        try:
            deadline = time.time() + max(30, timeout)
            while not getattr(server, "result", None) and time.time() < deadline:
                server.timeout = max(1.0, min(5.0, deadline - time.time()))  # type: ignore[union-attr]
                server.handle_request()  # type: ignore[union-attr]
        finally:
            server.server_close()  # type: ignore[union-attr]
        result = getattr(server, "result", {}) or {}
        if result.get("error"):
            raise StockTwitsMCPError(f"authorization failed: {result['error'][0]}")
        if result.get("state", [None])[0] != state:
            raise StockTwitsMCPError("authorization state did not match")
        code = result.get("code", [None])[0]

    if not code:
        raise StockTwitsMCPError("no authorization code was received")

    tokens = _post_form(metadata["token_endpoint"], {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
        "client_id": client_id,
        "code_verifier": verifier,
        "resource": mcp_url,
    })
    if not tokens.get("access_token"):
        raise StockTwitsMCPError("token exchange returned no access_token")
    token = {
        "access_token": tokens["access_token"],
        "refresh_token": tokens.get("refresh_token"),
        "expires_at": _now_ms() + int(tokens.get("expires_in", 3600)) * 1000,
        "token_endpoint": metadata["token_endpoint"],
        "client_id": client_id,
        "resource": mcp_url,
        "scope": tokens.get("scope") or scope,
        "saved_at": _now_ms(),
    }
    save_token(token)
    reset_client()
    return token


def _post_json(url: str, payload: dict, timeout: float = _TIMEOUT) -> dict:
    status, _, raw = _request(
        url,
        "POST",
        json.dumps(payload).encode(),
        {"Content-Type": "application/json", "Accept": "application/json"},
        timeout,
    )
    if status not in (200, 201):
        raise StockTwitsMCPError(f"{url} returned HTTP {status}: {raw[:300].decode(errors='replace')}")
    try:
        return json.loads(raw)
    except ValueError as exc:
        raise StockTwitsMCPError(f"{url} returned an unreadable response") from exc
