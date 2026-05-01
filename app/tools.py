"""Tool definitions for the ReAct agent.

Two tools: search_transcripts and submit_answer. Schemas are in Responses
API flat shape (name/description/parameters at top level of each tool).

Design choice: citations are IDs only ({video_id, start_ts, end_ts}).
The agent never writes chunk text into citations, so there's nothing to
fabricate or paraphrase-as-quote. The controller validates citation
existence on submit_answer; the frontend renders authoritative chunk
text via index lookup at display time.

Timestamps are integer seconds (chunks are fixed 30s windows; integer
seconds is the canonical form set at ingest time).

**Why submit_answer is a tool, not a plain message:**
- Structured citations for free:
    - The tool schema forces {video_id, start_ts, end_ts} as typed fields.
    - Plain messages would mean regex-parsing citations out of prose — fragile and unreliable.
- Unambiguous stopping signal:
    - "Agent is done" = "submit_answer was called." One line of code.
    - With plain messages, "no tool call this turn" could mean done, or confused, or giving up — you'd need heuristics.
- Controller can force termination:
    - tool_choice={"type": "function", "name": "submit_answer"} only works if it's a tool.
    - This is how the budget-exhaustion gate is implemented.
- Validation at the boundary:
    - Citations get checked against the index before the answer is accepted.
    - Fabricated citations are caught and the agent retries.
    - With plain text, validation happens after the fact — whatever the model wrote is what the user sees.
- Eval harness stays simple:
    - run_agent() returns {answer, citations} as a typed object.
    - Retrieval F1 is computed directly. No parsing layer between the agent and the metrics.
"""
import json
from typing import Any

from pydantic import BaseModel, ValidationError
from langfuse import observe

from app.config import settings
from app.retrieval import search, Mode

# ---------------------------------------------------------------------------
# Tool schemas (Responses API flat shape)
# ---------------------------------------------------------------------------

SEARCH_TRANSCRIPTS_SCHEMA: dict = {
    "type": "function",
    "name": "search_transcripts",
    "description": (
        "Search the video transcript corpus for chunks relevant to a query. "
        "Returns up to k chunks with video_id, title, timestamps, and a snippet. "
        "Use multiple searches with different phrasings to improve coverage; "
        "bounded-corpus deep research has no redundancy — a miss is unrecoverable."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Search query. Short, specific phrasing works best.",
            },
            "k": {
                "type": "integer",
                "description": f"Number of results to return. Default {settings.retrieval_k}.",
                "minimum": 1,
                "maximum": 20,
            },
        },
        "required": ["query"],
        "additionalProperties": False,
    },
}

SUBMIT_ANSWER_SCHEMA: dict = {
    "type": "function",
    "name": "submit_answer",
    "description": (
        "Submit the final answer. Call this exactly once, when you have gathered "
        "sufficient evidence. Every factual claim in the answer should be supported "
        "by at least one citation. Citations reference chunks by (video_id, start_ts, "
        "end_ts) in integer seconds; the controller validates existence."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "answer": {
                "type": "string",
                "description": "The final answer in markdown. Cite claims inline by referring to the citation list below.",
            },
            "citations": {
                "type": "array",
                "description": "List of chunks cited in the answer. IDs only.",
                "items": {
                    "type": "object",
                    "properties": {
                        "video_id": {"type": "string"},
                        "start_ts": {"type": "integer"},
                        "end_ts": {"type": "integer"},
                    },
                    "required": ["video_id", "start_ts", "end_ts"],
                    "additionalProperties": False,
                },
            },
        },
        "required": ["answer", "citations"],
        "additionalProperties": False,
    },
}

TOOLS: list[dict] = [SEARCH_TRANSCRIPTS_SCHEMA, SUBMIT_ANSWER_SCHEMA]


# ---------------------------------------------------------------------------
# Result types
# ---------------------------------------------------------------------------


class Citation(BaseModel):
    video_id: str
    start_ts: int
    end_ts: int


class SubmittedAnswer(BaseModel):
    answer: str
    citations: list[Citation]


class DispatchResult(BaseModel):
    """What dispatch() returns to the agent loop."""

    output_item: dict  # the function_call_output item to append to input_items
    terminal: bool = False  # True if submit_answer was called; loop should stop
    submitted: SubmittedAnswer | None = None


# ---------------------------------------------------------------------------
# Dispatch
# ---------------------------------------------------------------------------

@observe(name="dispatch_tool")
def dispatch(function_call_item: dict, channel: str, mode: Mode) -> DispatchResult:
    """Execute a function_call item from response.output.

    Returns a DispatchResult containing the function_call_output item to
    append to input_items for the next turn, plus a terminal flag and the
    parsed answer on submit_answer.

    Tool errors become function_call_output items (not exceptions) so the
    agent can recover — e.g., retry a search with different terms.
    """
    name = function_call_item["name"]
    call_id = function_call_item["call_id"]
    raw_args = function_call_item.get("arguments", "{}")

    try:
        args = json.loads(raw_args)
    except json.JSONDecodeError as e:
        return _error_output(call_id, f"Invalid JSON in tool arguments: {e}")

    if name == "search_transcripts":
        return _handle_search(call_id, args, channel, mode)
    if name == "submit_answer":
        return _handle_submit(call_id, args, channel)
    return _error_output(call_id, f"Unknown tool: {name}")


def _handle_search(call_id: str, args: dict[str, Any], channel: str, mode: Mode) -> DispatchResult:
    query = args.get("query")
    if not query or not isinstance(query, str):
        return _error_output(call_id, "search_transcripts requires a non-empty 'query' string.")

    k = args.get("k", settings.retrieval_k)
    try:
        hits = search(query, channel=channel, k=k, mode=mode)
    except Exception as e:
        return _error_output(call_id, f"search failed: {e}")

    # Tool return granularity (master plan Phase 2, v4.2): search returns
    # title + timestamp + short snippet. Truncating text keeps the search
    # phase context-cheap. Phase 2 will add read_video_segment for the
    # agent to escalate to full chunk text when needed.
    results = [
        {
            "video_id": h["video_id"],
            "title": h["title"],
            "start_ts": h["start_ts"],
            "end_ts": h["end_ts"],
            "snippet": _snippet(h["text"], max_chars=500),
        }
        for h in hits
    ]

    output = {
        "type": "function_call_output",
        "call_id": call_id,
        "output": json.dumps({"hits": results}),
    }
    return DispatchResult(output_item=output, terminal=False)


def _handle_submit(call_id: str, args: dict[str, Any], channel: str) -> DispatchResult:
    try:
        submitted = SubmittedAnswer(**args)
    except ValidationError as e:
        return _error_output(call_id, f"submit_answer arguments invalid: {e}")

    # Validate each citation exists in the index by exact (video_id, start_ts).
    invalid: list[str] = []
    for i, c in enumerate(submitted.citations):
        if not _citation_exists(c, channel):
            invalid.append(
                f"citation {i}: no chunk found for video_id={c.video_id} "
                f"start_ts={c.start_ts}"
            )

    if invalid:
        msg = "Citations failed validation:\n" + "\n".join(invalid)
        return _error_output(call_id, msg)

    output = {
        "type": "function_call_output",
        "call_id": call_id,
        "output": json.dumps({"status": "accepted"}),
    }
    return DispatchResult(output_item=output, terminal=True, submitted=submitted)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _error_output(call_id: str, message: str) -> DispatchResult:
    output = {
        "type": "function_call_output",
        "call_id": call_id,
        "output": json.dumps({"error": message}),
    }
    return DispatchResult(output_item=output, terminal=False)


def _snippet(text: str, max_chars: int = 500) -> str:
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 1].rstrip() + "…"


def _citation_exists(c: Citation, channel: str) -> bool:
    from app.retrieval import chunk_exists
    return chunk_exists(video_id=c.video_id, start_ts=c.start_ts, channel=channel)