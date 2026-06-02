"""ReAct agent loop over the transcript corpus."""
import asyncio
import json
from langfuse import observe, get_client

from app.config import settings
from app.llm import respond, to_input_item
from app.prompts import load_recipe
from app.retrieval import Mode
from app.tools import TOOLS, dispatch, SubmittedAnswer


_RECIPE_METADATA, SYSTEM_PROMPT = load_recipe()


def _noop(event: dict) -> None:
    """Default event sink: drops events when no caller is listening."""


class AgentResult(SubmittedAnswer):
    """The final agent output: answer + citations + run metadata."""

    steps_used: int
    budget_exhausted: bool


def _finalize(submitted: SubmittedAnswer, steps_used: int, budget_exhausted: bool) -> AgentResult:
    result = AgentResult(
        answer=submitted.answer,
        citations=submitted.citations,
        steps_used=steps_used,
        budget_exhausted=budget_exhausted,
    )
    langfuse = get_client()
    langfuse.update_current_span(
        metadata={"steps_used": steps_used, "budget_exhausted": budget_exhausted},
    )
    return result


@observe(name="run_agent")
async def run_agent(query: str, channel: str, mode: Mode, event_sink=_noop) -> AgentResult:
    """Run the ReAct loop for a single query.

    Returns AgentResult on success. Raises RuntimeError if the agent
    emits text without calling any tool (unexpected state) or if the
    forced submit_answer on budget exhaustion also fails.
    """
    langfuse = get_client()
    langfuse.update_current_span(
        input={"query": query, "channel": channel},
        metadata={"agent_model": settings.agent_model,
                  "reasoning_effort": settings.reasoning_effort,
                  "max_steps": settings.agent_max_steps,
                  "channel": channel,
                  "mode": mode,
                  "recipe_version": _RECIPE_METADATA.version},
    )

    input_items: list[dict] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user",   "content": query},
    ]

    # Monotonic search_id counter, spans the whole run.
    # See planning_docs/day-4-sse-contract.md for why.
    search_id_counter = 0

    def emit(event: dict) -> None:
        event_sink(event)  # event_sink defaults to _noop, so this is always safe to call.

    async def _dispatch_with_events(call_item, search_id):
        # Run one tool call and wrap it with its SSE progress events, so the whole
        # unit can be handed to asyncio.gather and run concurrently with the others.
        # For search_transcripts: emit search_start before the call, search_complete
        # after, both tagged with search_id so the frontend can pair them even when
        # parallel searches finish out of order. Non-search calls (search_id=None)
        # just dispatch with no events.
        if call_item["name"] == "search_transcripts":
            args = json.loads(call_item.get("arguments", "{}"))
            emit({"type": "search_start", "search_id": search_id, "query": args.get("query", "")})
        result = await dispatch(call_item, channel=channel, mode=mode)
        if call_item["name"] == "search_transcripts":
            parsed = json.loads(result.output_item["output"])
            result_count = len(parsed.get("hits", [])) if "hits" in parsed else 0
            emit({"type": "search_complete", "search_id": search_id, "result_count": result_count})
        return result

    for step in range(settings.agent_max_steps):
        response = await respond(input_items, tools=TOOLS, tool_choice="required")

        # 1. Append every emitted item verbatim (reasoning, function_calls, messages).
        for item in response.output:
            input_items.append(to_input_item(item))

        # 2. Collect every function_call, then dispatch them in parallel.
        call_items = [
            to_input_item(item) for item in response.output if item.type == "function_call"
        ]
        any_function_call = bool(call_items)

        # Sync pre-pass: allocate a unique search_id per search_transcripts call
        # before gather kicks off, so ids stay deterministic regardless of the
        # order coroutines actually complete in.
        search_ids = []
        for call_item in call_items:
            if call_item["name"] == "search_transcripts":
                search_ids.append(search_id_counter)
                search_id_counter += 1
            else:
                search_ids.append(None)

        results = await asyncio.gather(*(
            _dispatch_with_events(call_item, sid)
            for call_item, sid in zip(call_items, search_ids)
        ))

        # 3. Append outputs in call order, short-circuiting at submit_answer.
        terminal = None
        for result in results:
            input_items.append(result.output_item)
            if result.terminal:
                terminal = result
                # Stop dispatching: any function_calls after submit_answer in the
                # same response.output are left without matching output_items in
                # input_items. This is safe only because we return immediately after
                # this turn — input_items is not read again. If you ever defer the
                # return or log input_items on exit, revisit this.
                break

        # 3. Exit on successful submit_answer.
        if terminal is not None:
            return _finalize(terminal.submitted, step + 1, False)

        # 4. Model emitted text with no tool call — unexpected in this loop.
        if not any_function_call:
            raise RuntimeError(
                f"Agent emitted text without calling any tool at step {step + 1}. "
                f"Output: {response.output_text!r}"
            )

    # 5. Budget exhausted — force submit_answer.
    input_items.append({
        "role": "user",
        "content": (
            "Step budget exhausted. Call submit_answer now with the best "
            "answer you can construct from evidence gathered so far. If "
            "evidence is insufficient, say so in the answer."
        ),
    })
    response = await respond(
        input_items,
        tools=TOOLS,
        tool_choice={"type": "function", "name": "submit_answer"},
    )
    for item in response.output:
        input_items.append(to_input_item(item))
    for item in response.output:
        if item.type == "function_call":
            result = await dispatch(to_input_item(item), channel=channel, mode=mode)
            input_items.append(result.output_item)
            if result.terminal:
                return _finalize(result.submitted, settings.agent_max_steps, True)

    raise RuntimeError("Forced submit_answer on budget exhaustion failed.")