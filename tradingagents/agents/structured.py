"""Shared helpers for invoking an agent with structured output and a graceful fallback.

The Portfolio Manager, Trader, and Research Manager all follow the same
canonical pattern:

1. At agent creation, wrap the LLM with ``with_structured_output(Schema)``
   so the model returns a typed Pydantic instance. If the provider does
   not support structured output (rare; mostly older Ollama models), the
   wrap is skipped and the agent uses free-text generation instead.
2. At invocation, run the structured call and render the result back to
   markdown. A malformed or empty answer gets one corrective retry. If it
   still fails (the provider is down, or the model will not emit the
   schema), fall back to a plain ``llm.invoke`` so the pipeline never
   blocks.

Centralising the pattern here keeps the agent factories small and ensures
all three agents log the same warnings when fallback fires.
"""

from __future__ import annotations

import logging
from collections.abc import Callable
from typing import Any, TypeVar

from pydantic import BaseModel

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)

# Schema-only structured output binds exactly one tool (the schema itself), so a
# model that reaches for a search tool emits an unknown tool call and the whole
# structured attempt is discarded for a free-text retry. Agents on this path
# state the constraint explicitly rather than relying on the binding alone
# (#1130).
NO_EXTERNAL_TOOLS = (
    "Use only the evidence provided in this prompt. Do not call external tools "
    "or search the web; if something is missing, say so explicitly."
)


def bind_structured(llm: Any, schema: type[T], agent_name: str) -> Any | None:
    """Return ``llm.with_structured_output(schema)`` or ``None`` if unsupported.

    Logs a warning when the binding fails so the user understands the agent
    will use free-text generation for every call instead of one-shot fallback.
    """
    try:
        return llm.with_structured_output(schema)
    except (NotImplementedError, AttributeError) as exc:
        logger.warning(
            "%s: provider does not support with_structured_output (%s); "
            "falling back to free-text generation",
            agent_name, exc,
        )
        return None


_CORRECTIVE_RETRY = (
    "Your previous answer did not match the required structured schema. "
    "Answer again with only the schema's fields and no prose outside them."
)


def _with_corrective_retry(prompt: Any) -> Any:
    """``prompt`` plus a short instruction to answer in the schema.

    Supports the three shapes the agents pass: a string, a list of role/content
    dicts (Trader), and a list of LangChain messages (Sentiment). Anything else
    is returned unchanged, so an unknown prompt shape falls back as before.
    """
    if isinstance(prompt, str):
        return f"{prompt}\n\n{_CORRECTIVE_RETRY}"
    if isinstance(prompt, list):
        if prompt and isinstance(prompt[0], dict):
            return [*prompt, {"role": "user", "content": _CORRECTIVE_RETRY}]
        from langchain_core.messages import HumanMessage

        return [*prompt, HumanMessage(content=_CORRECTIVE_RETRY)]
    return prompt


def invoke_structured(structured_llm: Any | None, prompt: Any, agent_name: str) -> T | None:
    """Run the structured call; ``None`` when there is none or it fails twice.

    ``prompt`` is whatever the underlying LLM accepts (a string for chat
    invocations, a list of message dicts for chat models that take that
    shape), so a caller can forward the same value to its free-text fallback.

    A malformed or empty structured answer gets one corrective retry with the
    same schema before the free-text fallback. This is cheaper than falling
    back immediately, and it does not change the typed contract when it works.
    """
    if structured_llm is None:
        return None
    for attempt, candidate in enumerate((prompt, _with_corrective_retry(prompt)), start=1):
        try:
            result = structured_llm.invoke(candidate)
            if result is None:
                # A thinking model can answer in plain text instead of calling
                # the tool, leaving the parser with nothing to return.
                raise ValueError("structured output returned no parsed result")
            return result
        except Exception as exc:
            if attempt == 1:
                logger.info(
                    "%s: structured-output attempt failed (%s); correcting once",
                    agent_name, exc,
                )
            else:
                logger.warning(
                    "%s: structured-output invocation failed (%s); falling back to free text",
                    agent_name, exc,
                )
    return None


def invoke_structured_or_freetext(
    structured_llm: Any | None,
    plain_llm: Any,
    prompt: Any,
    render: Callable[[T], str],
    agent_name: str,
) -> str:
    """Run the structured call and render to markdown; fall back to free-text on any failure."""
    result = invoke_structured(structured_llm, prompt, agent_name)
    if result is not None:
        return render(result)
    return plain_llm.invoke(prompt).content
