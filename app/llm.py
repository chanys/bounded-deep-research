"""OpenAI Responses API wrappers.

Three call patterns, deliberately separated:
- respond(): multi-turn with tools, for the ReAct agent loop
- call_text_llm(): single-shot text -> text, for summarization (Phase 2)
- call_structured_llm(): single-shot text -> Pydantic, for judges (Phase 4)

Stateless mode (store=False); the ReAct loop owns its message history.
"""
from typing import TypeVar

from langfuse.openai import OpenAI
from openai.types.responses import Response
from pydantic import BaseModel

from app.config import settings

client = OpenAI(api_key=settings.openai_api_key)

T = TypeVar("T", bound=BaseModel)


def respond(
    input_items: list[dict],
    tools: list[dict] | None = None,
    tool_choice: str | dict = "auto",  # Model decides: either emit a text message, or call one (or more) of the tools.
) -> Response:
    """Multi-turn call for the ReAct agent loop.

    input_items accumulates across turns (messages + function_call +
    function_call_output items); the caller owns conversation history.
    Returns the raw Response so the caller can iterate response.output
    to dispatch function_call items and read token usage.
    """
    kwargs: dict = {
        "model": settings.agent_model,
        "input": input_items,
        "reasoning": {"effort": settings.reasoning_effort},
        "store": False,  # tells the Responses API: don't persist this request/response server-side
        "include": ["reasoning.encrypted_content"],
    }
    if tools:
        kwargs["tools"] = tools
        kwargs["tool_choice"] = tool_choice
    return client.responses.create(**kwargs)


def call_text_llm(system: str, user: str) -> str:
    """Single-shot text-in, text-out. For the summarization sub-agent."""
    response = client.responses.create(
        model=settings.agent_model,
        reasoning={"effort": settings.reasoning_effort},
        input=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        store=False,
    )
    return response.output_text


def call_structured_llm(
    system: str,
    user: str,
    response_model: type[T],
) -> T:
    """Single-shot text-in, Pydantic-out. For calibrated judges (Phase 4).
    """
    response = client.responses.parse(
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
    d.pop("status", None)
    return d
