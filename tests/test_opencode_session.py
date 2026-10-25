"""OpenCode Go session headers (x-opencode-session + identifying user agent).

The Go router rejects requests without a stable ``x-opencode-session``
(400 MissingSessionID) and asks clients to identify themselves instead of
sending the SDK's user agent. Verifies the header pair is attached exactly
for opencode.ai endpoints, that the session ID is stable per process and
pinnable via ``TRADINGAGENTS_LLM_SESSION_ID``, and that no other endpoint
sees any of it.
"""

import pytest

from tradingagents import __version__
from tradingagents.llm_clients.factory import create_llm_client
from tradingagents.llm_clients.opencode_session import (
    is_opencode_endpoint,
    request_headers,
    session_id,
)


@pytest.mark.unit
def test_opencode_endpoint_detection():
    assert is_opencode_endpoint("https://opencode.ai/zen/go/v1") is True
    assert is_opencode_endpoint("opencode.ai/zen/go/v1") is True  # scheme-less
    assert is_opencode_endpoint("https://inference.opencode.ai/go/openai/v1") is True
    # A suffix impostor is not a subdomain.
    assert is_opencode_endpoint("https://notopencode.ai/v1") is False
    assert is_opencode_endpoint("https://api.deepseek.com") is False
    assert is_opencode_endpoint("http://localhost:8000/v1") is False
    assert is_opencode_endpoint(None) is False


@pytest.mark.unit
def test_headers_only_for_opencode(monkeypatch):
    monkeypatch.delenv("TRADINGAGENTS_LLM_SESSION_ID", raising=False)
    headers = request_headers("https://opencode.ai/zen/go/v1")
    assert headers is not None
    assert set(headers) == {"x-opencode-session", "User-Agent"}
    assert headers["User-Agent"] == f"tradingagents/{__version__}"
    assert request_headers("http://localhost:8000/v1") is None
    assert request_headers(None) is None


@pytest.mark.unit
def test_session_id_stable_within_process(monkeypatch):
    monkeypatch.delenv("TRADINGAGENTS_LLM_SESSION_ID", raising=False)
    assert session_id() == session_id()
    assert session_id() == request_headers("https://opencode.ai/zen/go/v1")["x-opencode-session"]


@pytest.mark.unit
def test_session_id_env_override(monkeypatch):
    monkeypatch.setenv("TRADINGAGENTS_LLM_SESSION_ID", "sess-pinned-123")
    assert session_id() == "sess-pinned-123"
    assert request_headers("https://opencode.ai/zen/go/v1")["x-opencode-session"] == "sess-pinned-123"


@pytest.mark.unit
def test_get_llm_attaches_headers_for_opencode(monkeypatch):
    monkeypatch.delenv("TRADINGAGENTS_LLM_SESSION_ID", raising=False)
    llm = create_llm_client(
        provider="openai_compatible", model="minimax-m3", base_url="https://opencode.ai/zen/go/v1"
    ).get_llm()
    assert llm.default_headers["x-opencode-session"] == session_id()
    assert llm.default_headers["User-Agent"] == f"tradingagents/{__version__}"


@pytest.mark.unit
def test_get_llm_no_headers_elsewhere():
    llm = create_llm_client(
        provider="openai_compatible", model="qwen2.5", base_url="http://localhost:8000/v1"
    ).get_llm()
    assert llm.default_headers is None
