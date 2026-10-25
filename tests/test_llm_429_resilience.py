"""Client-level resilience to transient 429 capacity errors (#opencode-go).

The openai SDK already retries 429s honoring Retry-After with capped
exponential backoff; these tests prove the OpenAI-compatible client rides one
transient capacity blip out, fails with a clear upstream-capacity message once
the retry budget is spent, and leaves unconfigured providers at SDK defaults.
The HTTP layer is mocked (httpx2.MockTransport, the transport the openai SDK
3.37 speaks); no live endpoint is contacted.
"""

import httpx2
import openai
import pytest
from langchain_core.messages import HumanMessage

from tradingagents.llm_clients.factory import build_llm_kwargs
from tradingagents.llm_clients.openai_client import (
    LLMCapacityError,
    LocalCompatibleChatOpenAI,
)

# A mock chat-completion body the SDK parses happily, with no API key ever in play.
_CHAT_200 = {
    "id": "chatcmpl-mock",
    "object": "chat.completion",
    "created": 1735689600,
    "model": "glm-5.3-flash",
    "choices": [
        {"index": 0, "message": {"role": "assistant", "content": "ok"}, "finish_reason": "stop"}
    ],
    "usage": {"prompt_tokens": 1, "completion_tokens": 1, "total_tokens": 2},
}

_CAPACITY_429 = {
    "error": {
        "type": "server_error",
        "message": "Upstream request failed: [ttft_admission_refused] "
        "the cell is at capacity; retry shortly (after 18 s)",
    }
}

# The SDK honors retry-after-ms verbatim (divided by 1000), so a tiny value keeps
# the retry sleeps in the milliseconds: the sleeps themselves are time.sleep().
_MS_HINT = 20


def _transport(scripts):
    """A MockTransport serving each response from ``scripts`` in order.

    ``scripts`` items are dicts of status/headers/json; the last one repeats when
    the scripts run out (a "forever 429" mock). Requests are only counted, never
    logged with headers, so no Authorization value can leak into test output.
    """
    calls = []

    def handler(request: httpx2.Request) -> httpx2.Response:
        calls.append(request)
        script = scripts[min(len(calls) - 1, len(scripts) - 1)]
        return httpx2.Response(script["status"], headers=script.get("headers", {}), json=script.get("json", {}))

    client = httpx2.Client(transport=httpx2.MockTransport(handler))
    return client, calls


def _chat(**overrides):
    kwargs = {
        "model": "glm-5.3-flash",
        "base_url": "https://opencode.ai/inference/go/openai/v1",
        "api_key": "mock-key",
        "max_retries": 3,
        "timeout": 10.0,
    }
    kwargs.update(overrides)
    return LocalCompatibleChatOpenAI(**kwargs)


def test_one_429_with_retry_after_then_200_succeeds():
    """A single transient capacity blip is retried (honoring the hint) and succeeds."""
    retrying_contact, calls = _transport(
        [
            {"status": 429, "headers": {"retry-after-ms": str(_MS_HINT)}, "json": _CAPACITY_429},
            {"status": 200, "json": _CHAT_200},
        ]
    )
    llm = _chat(http_client=retrying_contact)

    assert llm.invoke([HumanMessage("hi")]).content == "ok"
    assert len(calls) == 2


def test_every_429_fails_after_the_retry_cap_with_a_clear_message():
    """Sustained capacity refusal ends in a clearly explained failure, not a hang."""
    budget_exhausted, calls = _transport(
        [{"status": 429, "headers": {"retry-after-ms": str(_MS_HINT)}, "json": _CAPACITY_429}]
    )
    llm = _chat(max_retries=2, http_client=budget_exhausted)

    with pytest.raises(LLMCapacityError) as caught:
        llm.invoke([HumanMessage("hi")])

    message = str(caught.value)
    assert "at capacity" in message
    assert "glm-5.3-flash" in message
    assert "Rerun later" in message
    # SDK attempts are exhausted first (1 initial + 2 retries); nothing loops
    # beyond the budget once the endpoint insists it is at capacity.
    assert len(calls) == 3
    assert isinstance(caught.value.__cause__, openai.RateLimitError)


def test_the_clear_message_never_carries_the_api_key():
    """The raised explanation describes the cause without echoing credentials."""
    budget_exhausted, _ = _transport(
        [{"status": 429, "headers": {"retry-after-ms": str(_MS_HINT)}, "json": _CAPACITY_429}]
    )
    llm = _chat(max_retries=0, http_client=budget_exhausted)

    with pytest.raises(LLMCapacityError) as caught:
        llm.invoke([HumanMessage("hi")])

    assert "mock-key" not in str(caught.value)
    assert "mock-key" not in repr(caught.value)


def test_unconfigured_providers_keep_sdk_defaults():
    """Provider defaults survive unless a value is explicitly set."""
    assert build_llm_kwargs({"llm_provider": "openai_compatible"}) == {}

    explicit = build_llm_kwargs(
        {"llm_provider": "openai_compatible", "llm_max_retries": "6", "llm_timeout": "45"}
    )
    assert explicit == {"max_retries": 6, "timeout": 45.0}


def test_dependency_wiring_goes_the_same_route(tmp_path, monkeypatch):
    """The env overlay feeds the factory that builds the chat client."""
    from tradingagents.default_config import build_default_config

    monkeypatch.setenv("TRADINGAGENTS_LLM_TIMEOUT", "45")
    monkeypatch.setenv("TRADINGAGENTS_MAX_CONCURRENCY", "2")
    config = build_default_config()
    kwargs = build_llm_kwargs(config)

    assert kwargs["timeout"] == 45.0
    # The env overlay delivers a string; the graph layer coerces it before it
    # becomes a thread-pool size.
    assert config["max_concurrency"] == "2"
    from tradingagents.graph.propagation import Propagator

    assert Propagator(max_concurrency=config["max_concurrency"]).max_concurrency == 2
    assert Propagator().max_concurrency is None

    monkeypatch.delenv("TRADINGAGENTS_LLM_TIMEOUT")
    monkeypatch.delenv("TRADINGAGENTS_MAX_CONCURRENCY")
    env_free = build_llm_kwargs(build_default_config())
    assert "timeout" not in env_free and "max_retries" not in env_free
