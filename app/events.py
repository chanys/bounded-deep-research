"""SSE event contract for the /query stream.

These Pydantic models are the single source of truth for what the agent emits
over the wire. Each model has a literal `type` field that acts as a tag, so the
frontend can look at `type` and know exactly which shape it received. The
frontend keeps a matching set of these shapes (web/lib/events.ts).

How they're used: an emitter builds one of these models and sends
`model.model_dump()` (a plain dict); the queue/SSE layer turns that dict into a
`data: {...}` line on the stream.

Correlation: each search carries a counter id (search_id) assigned before the
searches run in parallel. Because parallel calls can finish out of order, the
client pairs a search_start event with its search_complete by that id rather
than by arrival order.
"""
from typing import Literal

from pydantic import BaseModel


class RunStarted(BaseModel):
    """First event of a run. Sent once, before any work, so the client knows the
    run's identity and configuration."""

    type: Literal["run_started"] = "run_started"   # event tag
    run_id: str                 # unique id for this run; key for GET /runs/{run_id}/evidence
    query: str                  # the user's question
    channel: str                # which corpus/channel is being searched
    mode: str                   # retrieval mode: bm25 | dense | hybrid
    recipe_version: str         # version of the prompt recipe driving the agent
    max_steps: int              # step budget, so the UI can show "steps used / budget"


class TurnStart(BaseModel):
    """Sent just before each model call (one step of the ReAct loop). The UI uses
    it to show that the model is thinking."""

    type: Literal["turn_start"] = "turn_start"      # event tag
    step: int                   # 0-based index of this turn within the run


class TurnComplete(BaseModel):
    """Sent right after a model call returns. Carries the token usage for that one
    turn, which the UI adds up and the evidence fold uses to compute cost."""

    type: Literal["turn_complete"] = "turn_complete"  # event tag
    step: int                   # matches the step from the TurnStart it pairs with
    usage: dict                 # this turn's token counts (TokenUsage-shaped)


class SearchStart(BaseModel):
    """Sent when the agent begins a transcript search, before any results are back."""

    type: Literal["search_start"] = "search_start"  # event tag
    search_id: int              # id used to pair this with its SearchComplete
    query: str                  # the search query the agent chose
    mode: str                   # retrieval mode used for this search


class SearchComplete(BaseModel):
    """Sent when a search returns its hits. Paired with its SearchStart by search_id."""

    type: Literal["search_complete"] = "search_complete"  # event tag
    search_id: int              # matches the search_id of the SearchStart
    result_count: int           # how many chunks the search returned
    returned_chunk_ids: list[str]   # canonical (padded) chunk_ids of those hits


class AnswerDelta(BaseModel):
    """A piece of the final answer, streamed as the model writes it (before the
    full AnswerComplete arrives). The client appends `text` to what it has so far."""

    type: Literal["answer_delta"] = "answer_delta"  # event tag
    text: str                   # newly produced answer text to append


class AnswerComplete(BaseModel):
    """Final event of a successful run. Carries the finished answer and the chunks
    it cites."""

    type: Literal["answer_complete"] = "answer_complete"  # event tag
    answer: str                 # the final answer text (markdown)
    citations: list[dict]       # cited chunks as [{video_id, start_ts, end_ts}]


class ErrorEvent(BaseModel):
    """Sent if the run fails. After this the stream closes."""

    type: Literal["error"] = "error"    # event tag
    message: str                # human-readable failure description


def usage_dict(response) -> dict:
    """Pull a flat token-usage dict out of a Responses API response.

    The API's usage object is sometimes absent and has optional nested detail
    objects, so every field is read defensively with a 0 fallback. Reasoning
    tokens are already counted inside output_tokens; we surface them separately
    for visibility but do not add them again.
    """
    u = getattr(response, "usage", None)
    if u is None:
        return {"input_tokens": 0, "cached_input_tokens": 0, "output_tokens": 0,
                "reasoning_tokens": 0, "total_tokens": 0}
    in_details = getattr(u, "input_tokens_details", None)
    out_details = getattr(u, "output_tokens_details", None)
    return {
        "input_tokens": getattr(u, "input_tokens", 0) or 0,
        "cached_input_tokens": getattr(in_details, "cached_tokens", 0) or 0,
        "output_tokens": getattr(u, "output_tokens", 0) or 0,
        "reasoning_tokens": getattr(out_details, "reasoning_tokens", 0) or 0,
        "total_tokens": getattr(u, "total_tokens", 0) or 0,
    }
