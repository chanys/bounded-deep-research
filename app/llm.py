"""OpenAI Responses API wrappers.

Three call patterns, deliberately separated:
- respond(): multi-turn with tools, for the ReAct agent loop
- call_text_llm(): single-shot text -> text, for summarization (Phase 2)
- call_structured_llm(): single-shot text -> Pydantic, for judges (Phase 4)

Stateless mode (store=False); the ReAct loop owns its message history.
"""
from typing import TypeVar

from langfuse.openai import AsyncOpenAI
from openai.types.responses import Response
from pydantic import BaseModel

from app.config import settings

client = AsyncOpenAI(api_key=settings.openai_api_key)

T = TypeVar("T", bound=BaseModel)


async def respond(
    input_items: list[dict],
    tools: list[dict] | None = None,
    tool_choice: str | dict = "auto",  # Model decides: either emit a text message, or call one (or more) of the tools.
    on_event=None,
) -> Response:
    """Multi-turn call for the ReAct agent loop.

    input_items accumulates across turns (messages + function_call +
    function_call_output items); the caller owns conversation history.
    Returns the raw Response so the caller can iterate response.output
    to dispatch function_call items and read token usage.

    If on_event is given, the call is run in streaming mode and on_event is
    invoked with each raw streaming event as it arrives (used to stream the final
    answer to the UI). The reconstructed final Response is still returned, so the
    caller's logic is unchanged either way.
    """
    reasoning: dict = {"effort": settings.reasoning_effort}
    if settings.reasoning_summary:
        reasoning["summary"] = settings.reasoning_summary  # readable summary of the reasoning

    kwargs: dict = {
        "model": settings.agent_model,
        "input": input_items,
        "reasoning": reasoning,
        "store": False,  # tells the Responses API: don't persist this request/response server-side
        "include": ["reasoning.encrypted_content"],  # return the reasoning (encrypted) in the response
    }
    if tools:
        kwargs["tools"] = tools
        kwargs["tool_choice"] = tool_choice

    if on_event is None:
        return await client.responses.create(**kwargs)

    # Streaming: forward every event to on_event, then return the final Response.
    # We use create(stream=True) (a plain async iterator) rather than the higher-
    # level .stream() context manager, which is broken in the langfuse-wrapped
    # client on this SDK version. The terminal "response.completed" event carries
    # the assembled final Response (output items, encrypted reasoning, usage).
    final: Response | None = None
    stream = await client.responses.create(**kwargs, stream=True)
    async for event in stream:
        on_event(event)
        if getattr(event, "type", None) == "response.completed":
            final = event.response
    if final is None:
        raise RuntimeError("Streaming response ended without a response.completed event.")
    return final


async def call_text_llm(system: str, user: str) -> str:
    """Single-shot text-in, text-out. For the summarization sub-agent."""
    response = await client.responses.create(
        model=settings.agent_model,
        reasoning={"effort": settings.reasoning_effort},
        input=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        store=False,
    )
    return response.output_text


async def call_structured_llm(
    system: str,
    user: str,
    response_model: type[T],
) -> T:
    """Single-shot text-in, Pydantic-out. For calibrated judges (Phase 4).
    """
    response = await client.responses.parse(
        model=settings.agent_model,
        reasoning={"effort": settings.reasoning_effort},
        input=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        text_format=response_model,
        store=False,
    )
    parsed = response.output_parsed
    if parsed is None:
        raise ValueError("Structured LLM response parsed to None.")
    return parsed


def to_input_item(item) -> dict:
    """Convert a response output item into an input-shaped dict.

    The Responses API has asymmetric schemas: output items include fields
    like `status` that the input schema rejects. Strip them before re-sending.
    """
    d = item.model_dump(exclude_none=True)
    d.pop("status", None)  # Without a default `None`, a missing key raises KeyError
    return d
