"""Anthropic (Claude) client for the eval side.

Kept separate from core/llm.py (the OpenAI client the agent uses) so each
provider's SDK and credential stay scoped to the code that needs them: the
serving app imports core.llm and never this module, while the offline eval code
imports this and never drags in the OpenAI client. The two APIs also share
almost no surface, so there is nothing to unify.

Cross-family on purpose: the agent runs on OpenAI, the eval judges run on the
Claude family, so a model never grades its own family's output.
"""
from typing import TypeVar

from anthropic import AsyncAnthropic
from pydantic import BaseModel

from core.config import settings

T = TypeVar("T", bound=BaseModel)

_client: AsyncAnthropic | None = None

# Opt-in per-call usage capture. Off by default (None), so scripts that don't enable it are
# unaffected. A caller enables it once, then reads usage_totals() to report actual token spend
# (the pre-spend cost print is only an estimate; this is the ground truth).
_usage: list[dict] | None = None


def enable_usage_capture() -> None:
    """Start (or reset) recording per-call token usage for later usage_totals()."""
    global _usage
    _usage = []


def usage_totals() -> dict | None:
    """Aggregate captured token usage, or None if capture was never enabled."""
    if _usage is None:
        return None
    return {
        "calls": len(_usage),
        "input_tokens": sum(c["input"] for c in _usage),
        "output_tokens": sum(c["output"] for c in _usage),
        "cache_read_input_tokens": sum(c["cache_read"] for c in _usage),
        "cache_creation_input_tokens": sum(c["cache_creation"] for c in _usage),
    }


def _get_client() -> AsyncAnthropic:
    """Construct the async Anthropic client once, lazily.

    Lazy so importing this module never requires ANTHROPIC_API_KEY; the key is
    needed only when a call is actually made.
    """
    global _client
    if _client is None:
        if not settings.anthropic_api_key:
            raise RuntimeError(
                "ANTHROPIC_API_KEY is not set; it is required for the eval-side "
                "Claude calls (summaries, judges). Add it to .env."
            )
        # Higher retry budget than the SDK default (2): the eval batches make
        # hundreds of calls, and a transient 429/5xx that slips through would
        # otherwise surface as a wrong result (e.g. a query wrongly judged
        # unanswerable during grounding).
        _client = AsyncAnthropic(api_key=settings.anthropic_api_key, max_retries=5)
    return _client


async def call_structured(
    system: str,
    user: str,
    response_model: type[T],
    *,
    model: str,
    max_tokens: int,
    thinking: dict | None = None,
) -> T:
    """Single-shot Claude call returning a validated Pydantic object.

    thinking=None omits the parameter, which on Sonnet 5 means adaptive thinking
    is on (its default). Pass {"type": "disabled"} to turn reasoning off, e.g.
    for the bulk summarization pass where it is not needed and would otherwise
    spend tokens on every call.
    """
    kwargs: dict = {
        "model": model,
        "max_tokens": max_tokens,
        "system": system,
        "messages": [{"role": "user", "content": user}],
        "output_format": response_model,
    }
    if thinking is not None:
        kwargs["thinking"] = thinking
    response = await _get_client().messages.parse(**kwargs)
    if _usage is not None:   # capture before the truncation guard: a truncated call still spends
        u = response.usage
        _usage.append({
            "input": getattr(u, "input_tokens", 0) or 0,
            "output": getattr(u, "output_tokens", 0) or 0,   # includes thinking tokens
            "cache_read": getattr(u, "cache_read_input_tokens", 0) or 0,
            "cache_creation": getattr(u, "cache_creation_input_tokens", 0) or 0,
        })
    parsed = response.parsed_output
    if parsed is None:
        raise ValueError(
            f"Claude structured response parsed to None "
            f"(stop_reason={getattr(response, 'stop_reason', '?')}; "
            f"raise max_tokens if it is 'max_tokens')."
        )
    return parsed
