"""StockTwits MCP client: transport, token handling, and vendor wiring.

These are unit tests: every HTTP call is mocked, and the autouse network guard
in conftest keeps a real socket from opening.
"""

from __future__ import annotations

import json
from unittest.mock import patch

import pytest

from tradingagents.dataflows.vendors import stocktwits, stocktwits_mcp


@pytest.mark.unit
class TestSSE:
    def test_event_stream_picks_the_matching_request(self):
        raw = (
            'event: message\ndata: {"jsonrpc":"2.0","method":"notifications/message"}\n\n'
            'event: message\ndata: {"jsonrpc":"2.0","id":7,"result":{"ok":true}}\n\n'
        )
        assert stocktwits_mcp._sse_payload(raw, want_id=7) == {
            "jsonrpc": "2.0", "id": 7, "result": {"ok": True},
        }

    def test_plain_json_is_accepted(self):
        raw = '{"jsonrpc":"2.0","id":1,"result":{"ok":true}}'
        assert stocktwits_mcp._sse_payload(raw)["result"] == {"ok": True}

    def test_unreadable_body_raises(self):
        with pytest.raises(stocktwits_mcp.StockTwitsMCPError):
            stocktwits_mcp._sse_payload("not json")


@pytest.mark.unit
class TestMessageNormalization:
    def test_top_level_sentiment_becomes_entities_shape(self):
        message = {
            "body": "$GOOGL bullish",
            "created_at": "2026-10-31T02:14:59Z",
            "sentiment": "Bullish",
            "user": {"username": "u"},
        }
        normalized = stocktwits_mcp._normalize_message(message)
        assert normalized["entities"]["sentiment"]["basic"] == "Bullish"
        assert normalized["body"] == "$GOOGL bullish"

    def test_missing_fields_get_safe_defaults(self):
        normalized = stocktwits_mcp._normalize_message({})
        assert normalized["body"] == ""
        assert normalized["created_at"] == ""
        assert normalized["user"] == {}


@pytest.mark.unit
class TestAvailability:
    def test_disabled_by_env(self, monkeypatch):
        monkeypatch.setenv("STOCKTWITS_MCP_DISABLE", "1")
        monkeypatch.setenv("STOCKTWITS_MCP_TOKEN", "token")
        assert stocktwits_mcp.available() is False

    def test_env_token_enables(self, monkeypatch):
        monkeypatch.delenv("STOCKTWITS_MCP_DISABLE", raising=False)
        monkeypatch.setenv("STOCKTWITS_MCP_TOKEN", "token")
        assert stocktwits_mcp.available() is True

    def test_token_file_enables(self, tmp_path, monkeypatch):
        monkeypatch.delenv("STOCKTWITS_MCP_DISABLE", raising=False)
        monkeypatch.delenv("STOCKTWITS_MCP_TOKEN", raising=False)
        monkeypatch.setenv("STOCKTWITS_AUTH_PATH", str(tmp_path / "auth.json"))
        stocktwits_mcp.save_token({"access_token": "a", "expires_at": 9_999_999_999_999})
        assert stocktwits_mcp.available() is True

    def test_no_token_means_unavailable(self, tmp_path, monkeypatch):
        monkeypatch.delenv("STOCKTWITS_MCP_DISABLE", raising=False)
        monkeypatch.delenv("STOCKTWITS_MCP_TOKEN", raising=False)
        monkeypatch.setenv("STOCKTWITS_AUTH_PATH", str(tmp_path / "missing.json"))
        assert stocktwits_mcp.available() is False


@pytest.mark.unit
class TestTokenLifecycle:
    def test_save_load_logout_roundtrip(self, tmp_path, monkeypatch):
        monkeypatch.setenv("STOCKTWITS_AUTH_PATH", str(tmp_path / "auth.json"))
        stocktwits_mcp.save_token({"access_token": "a", "refresh_token": "r"})
        assert stocktwits_mcp.load_token()["access_token"] == "a"
        assert stocktwits_mcp.logout() is True
        assert stocktwits_mcp.load_token() is None
        assert stocktwits_mcp.logout() is False

    def test_expired_token_is_refreshed_and_persisted(self, tmp_path, monkeypatch):
        monkeypatch.delenv("STOCKTWITS_MCP_TOKEN", raising=False)
        monkeypatch.setenv("STOCKTWITS_AUTH_PATH", str(tmp_path / "auth.json"))
        stocktwits_mcp.save_token({
            "access_token": "old",
            "refresh_token": "refresh",
            "client_id": "client",
            "token_endpoint": "https://example.test/token",
            "resource": "https://example.test/mcp",
            "expires_at": 1,  # long expired
        })
        seen = {}

        def fake_post(url, fields, timeout=None):
            seen.update(fields)
            return {"access_token": "new", "refresh_token": "rotated", "expires_in": 3600}

        with patch.object(stocktwits_mcp, "_post_form", fake_post):
            assert stocktwits_mcp._access_token() == "new"
        assert seen["grant_type"] == "refresh_token"
        assert seen["refresh_token"] == "refresh"
        assert stocktwits_mcp.load_token()["access_token"] == "new"
        assert stocktwits_mcp.load_token()["refresh_token"] == "rotated"

    def test_missing_refresh_details_raise_auth_required(self, tmp_path, monkeypatch):
        monkeypatch.delenv("STOCKTWITS_MCP_TOKEN", raising=False)
        monkeypatch.setenv("STOCKTWITS_AUTH_PATH", str(tmp_path / "auth.json"))
        stocktwits_mcp.save_token({"access_token": "old", "expires_at": 1})
        with pytest.raises(stocktwits_mcp.StockTwitsAuthRequired):
            stocktwits_mcp._access_token()


@pytest.mark.unit
class TestMCPClient:
    def test_initialize_then_call_keeps_session_id(self):
        calls = []

        def fake_request(url, method="GET", body=None, headers=None, timeout=20.0):
            calls.append(json.loads(body) if body else None)
            if len(calls) == 1:   # initialize
                return 200, {"Mcp-Session-Id": "session-1"}, (
                    'event: message\ndata: {"jsonrpc":"2.0","id":1,"result":{}}\n\n'
                ).encode()
            if len(calls) == 2:   # notifications/initialized
                return 202, {}, b""
            return 200, {}, (
                'event: message\ndata: {"jsonrpc":"2.0","id":2,'
                '"result":{"content":[{"type":"text","text":"{\\"ok\\":true}"}]}}\n\n'
            ).encode()

        with patch.object(stocktwits_mcp, "_request", fake_request):
            client = stocktwits_mcp._MCPClient("https://example.test/mcp", "token", 20.0)
            result = client.call_tool("get_symbol_messages", {"symbol": "GOOGL", "limit": 1})
        assert result["content"][0]["text"] == '{"ok":true}'
        assert calls[0]["method"] == "initialize"
        assert calls[1]["method"] == "notifications/initialized"
        assert calls[2]["params"]["name"] == "get_symbol_messages"


@pytest.mark.unit
class TestFetchMessages:
    def test_fetch_messages_parses_tool_json(self):
        class FakeClient:
            def call_tool(self, name, arguments):
                assert name == "get_symbol_messages"
                assert arguments == {"symbol": "GOOGL", "limit": 5}
                return {"content": [{"type": "text", "text": json.dumps({
                    "messages": [{"body": "$GOOGL up", "created_at": "2026-10-31T00:00:00Z",
                                  "sentiment": "Bullish", "user": {"username": "u"}}],
                })}]}

        with patch.object(stocktwits_mcp, "_access_token", lambda: "token"), \
                patch.object(stocktwits_mcp, "_client_for", lambda *a: FakeClient()):
            messages = stocktwits_mcp.fetch_messages("GOOGL", limit=5)
        assert messages[0]["body"] == "$GOOGL up"
        assert messages[0]["entities"]["sentiment"]["basic"] == "Bullish"


@pytest.mark.unit
class TestVendorWiring:
    def test_vendor_uses_mcp_when_available(self, monkeypatch):
        monkeypatch.setattr(stocktwits_mcp, "available", lambda: True)
        monkeypatch.setattr(stocktwits_mcp, "fetch_messages", lambda symbol, limit, timeout: [
            {"body": "MCP message", "created_at": "2026-10-31T00:00:00Z",
             "user": {"username": "u"}, "sentiment": "Bullish"},
        ])
        out = stocktwits.fetch_stocktwits_messages("GOOGL")
        assert "MCP message" in out
        assert "Total: 1" in out

    def test_vendor_degrades_with_login_hint_when_unauthenticated(self, monkeypatch):
        monkeypatch.setattr(stocktwits_mcp, "available", lambda: True)

        def boom(*_a, **_k):
            raise stocktwits_mcp.StockTwitsAuthRequired("no token")

        monkeypatch.setattr(stocktwits_mcp, "fetch_messages", boom)
        out = stocktwits.fetch_stocktwits_messages("GOOGL")
        assert out.startswith("<stocktwits unavailable")
        assert "stocktwits-login" in out
