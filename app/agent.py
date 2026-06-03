"""ReAct agent loop over the transcript corpus.

run_agent drives the loop. On each turn it calls the model, which either issues
tool calls (search_transcripts / read_video_segment) or finishes by calling
submit_answer. The tool calls within a turn run in parallel. The loop, not the
model, owns the running conversation (input_items) and emits progress events as
it goes; those same events are folded into RunEvidenceState for the Run Audit.
If the agent never submits within the step budget, a final turn forces it to.
"""
import asyncio
import json
from uuid import uuid4

from langfuse import observe, get_client

from app.config import settings
from app.evidence import EvidenceCollector, put_run
from app.events import (
    RunStarted, TurnStart, TurnComplete,
    SearchStart, SearchComplete, ReadStart, ReadComplete, usage_dict,
)
from app.llm import respond, to_input_item
from app.prompts import load_recipe
from app.retrieval import Mode
from app.tools import TOOLS, dispatch, SubmittedAnswer


_RECIPE_METADATA, SYSTEM_PROMPT = load_recipe()


def _noop(event: dict) -> None:
    """Default event sink: silently drops events when no caller is listening."""


class AgentResult(SubmittedAnswer):
    """The final agent output: the submitted answer and citations, plus a little
    metadata about how the run went."""

    steps_used: int             # how many turns the run took before submitting
    budget_exhausted: bool      # True if the run hit the step budget and was forced to answer


def _finalize(submitted: SubmittedAnswer, steps_used: int, budget_exhausted: bool) -> AgentResult:
    """Wrap the submitted answer in an AgentResult and record run metadata on the
    current Langfuse span."""
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
async def run_agent(query: str, channel: str, mode: Mode, event_sink=_noop, dump_dir=None) -> AgentResult:
    """Run the agent on one query and return its answer.

    The agent searches, reads, and finally calls submit_answer; this drives that
    loop and returns the submitted answer (plus citations and run metadata) as an
    AgentResult.

    Arguments:
      query:      the user's question.
      channel:    which corpus to search.
      mode:       retrieval strategy (bm25 | dense | hybrid).
      event_sink: optional callback that receives every progress event as it
                  happens. The SSE endpoint uses this to stream to the browser.
                  Defaults to a no-op, so the agent runs fine with no listener.
      dump_dir:   if set, write a human-readable markdown trace of the run to this
                  directory on success (see app.trace_dump). Left off for the
                  server so it doesn't write a file on every request; the
                  recipe-iteration batch runner turns it on.

    Raises RuntimeError in two cases that should not normally happen:
      - the model replies with plain text instead of calling a tool, or
      - the final forced submit_answer (after the step budget runs out) does not
        actually submit.
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

    # The conversation history. The loop appends to it every turn; the model is
    # stateless (store=False), so this list is the only memory of the run.
    input_items: list[dict] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user",   "content": query},
    ]

    # run_id = langfuse trace_id (gives a free cross-link to the trace for the
    # cost link-outs); fall back to a random id if tracing is disabled.
    run_id = langfuse.get_current_trace_id() or uuid4().hex
    trace_url = langfuse.get_trace_url()

    # Folds the same event stream the SSE emits into RunEvidenceState for the audit.
    collector = EvidenceCollector(
        run_id=run_id, query=query, channel=channel,
        recipe_version=_RECIPE_METADATA.version, retrieval_mode=mode,
        trace_url=trace_url, model=settings.agent_model,
    )

    def emit(event: dict) -> None:
        """Send one event to both consumers: the external sink (the browser via
        SSE, or _noop when nobody is listening) and the evidence collector."""
        event_sink(event)
        collector.handle(event)

    emit(RunStarted(run_id=run_id, query=query, channel=channel, mode=mode,
                    recipe_version=_RECIPE_METADATA.version).model_dump())

    # Counters for the per-search and per-read ids. They span the whole run and
    # are handed out in a sync pre-pass (below) before the parallel dispatch, so
    # an id is fixed before its coroutine starts, regardless of finish order.
    search_id_counter = 0
    read_id_counter = 0

    async def _respond_turn(step, tool_choice):
        """Make one model call and wrap it in two events: a turn_start just before,
        and a turn_complete just after. The turn_complete reports how many tokens
        this call used, which the UI shows as a token count and the evidence fold
        adds up into the run's total cost."""
        emit(TurnStart(step=step).model_dump())
        response = await respond(input_items, tools=TOOLS, tool_choice=tool_choice)
        emit(TurnComplete(step=step, usage=usage_dict(response)).model_dump())
        return response

    async def _dispatch_with_events(call_item, kind, ev_id):
        """Run one tool call and emit its progress events around it.

        For a search or a read, this sends a start event before the call and a
        complete event after. Both events carry the same ev_id (the search_id or
        read_id), which is how the frontend knows the "complete" belongs to that
        "start". The id matters because several tool calls in a turn run at the
        same time and can finish in any order, so arrival order alone is not
        enough to match them up.

        Other tools, like submit_answer, just run with no events.

        Because this bundles the events with the call into one coroutine, the loop
        can launch several of these at once with asyncio.gather and let them run
        concurrently.
        """
        if kind == "search":
            args = json.loads(call_item.get("arguments", "{}"))
            emit(SearchStart(search_id=ev_id, query=args.get("query", ""), mode=mode).model_dump())
        elif kind == "read":
            args = json.loads(call_item.get("arguments", "{}"))
            emit(ReadStart(read_id=ev_id, video_id=args.get("video_id", ""),
                           start_ts=int(args.get("start_ts", 0))).model_dump())

        result = await dispatch(call_item, channel=channel, mode=mode)

        if kind == "search":
            # Rebuild the canonical chunk_ids from the hits for the evidence fold.
            hits = json.loads(result.output_item["output"]).get("hits", [])
            chunk_ids = [f"{h['video_id']}:{int(h['start_ts']):05d}" for h in hits]
            emit(SearchComplete(search_id=ev_id, result_count=len(hits),
                                returned_chunk_ids=chunk_ids).model_dump())
        elif kind == "read":
            parsed = json.loads(result.output_item["output"])
            if "text" in parsed:   # the chunk was found
                cid = f"{parsed['video_id']}:{int(parsed['start_ts']):05d}"
                emit(ReadComplete(read_id=ev_id, ok=True, chunk_id=cid,
                                  video_id=parsed["video_id"], start_ts=parsed["start_ts"],
                                  end_ts=parsed["end_ts"]).model_dump())
            else:   # not found / error came back as the tool result
                emit(ReadComplete(read_id=ev_id, ok=False).model_dump())
        return result

    def _finish(result: AgentResult) -> AgentResult:
        """Wrap up a successful run and return its result.

        Every success path goes through here so the wrap-up happens in one place:
        save the run's evidence (the collector turns the events it saw into the
        final RunEvidenceState), and, if dump_dir was given, write the markdown
        trace of the run. It then returns the result unchanged.

        Note: it reuses the run_id and trace_url captured at the top of run_agent.
        Those must be read there, not here, because they are only available while
        the @observe span is active.
        """
        put_run(collector.finalize(result))
        if dump_dir is not None:
            from app.trace_dump import write_trace_dump
            write_trace_dump(
                dump_dir,
                query=query,
                channel=channel,
                mode=mode,
                recipe_version=_RECIPE_METADATA.version,
                trace_id=run_id,
                trace_url=trace_url,
                input_items=input_items,
                result=result,
            )
        return result

    for step in range(settings.agent_max_steps):
        response = await _respond_turn(step, tool_choice="required")

        # 1. Append everything the model emitted, verbatim (reasoning, function_calls, messages).
        for item in response.output:
            input_items.append(to_input_item(item))

        # 2. Collect this turn's function_calls and assign each search/read its id.
        #    The pre-pass is synchronous so ids are fixed before the parallel
        #    dispatch starts. slots holds (kind, ev_id); kind "search" | "read" |
        #    other tool name (no events for the latter).
        call_items = [
            to_input_item(item) for item in response.output if item.type == "function_call"
        ]
        any_function_call = bool(call_items)

        slots: list[tuple[str, int | None]] = []
        for call_item in call_items:
            name = call_item["name"]
            if name == "search_transcripts":
                slots.append(("search", search_id_counter))
                search_id_counter += 1
            elif name == "read_video_segment":
                slots.append(("read", read_id_counter))
                read_id_counter += 1
            else:
                slots.append((name, None))

        # 3. Dispatch all of this turn's tool calls in parallel.
        results = await asyncio.gather(*(
            _dispatch_with_events(call_item, kind, ev_id)
            for call_item, (kind, ev_id) in zip(call_items, slots)
        ))

        # 4. Append the tool outputs in call order, stopping at submit_answer.
        terminal = None
        for result in results:
            input_items.append(result.output_item)
            if result.terminal:
                terminal = result
                # Stop here: any function_calls after submit_answer in the same
                # response.output are left without matching output_items in
                # input_items. That is safe only because we return immediately
                # after this turn, so input_items is never read again. If you ever
                # defer the return or log input_items on exit, revisit this.
                break

        # 5. Exit on a successful submit_answer.
        if terminal is not None:
            return _finish(_finalize(terminal.submitted, step + 1, False))

        # 6. The model produced no tool call. Unexpected, since tool_choice is
        #    "required", so treat it as an error rather than looping forever.
        if not any_function_call:
            raise RuntimeError(
                f"Agent emitted text without calling any tool at step {step + 1}. "
                f"Output: {response.output_text!r}"
            )

    # 7. Step budget exhausted without an answer. Force one last turn that must
    #    call submit_answer (tool_choice pins it to that single tool).
    input_items.append({
        "role": "user",
        "content": (
            "Step budget exhausted. Call submit_answer now with the best "
            "answer you can construct from evidence gathered so far. If "
            "evidence is insufficient, say so in the answer."
        ),
    })
    response = await _respond_turn(
        settings.agent_max_steps,
        tool_choice={"type": "function", "name": "submit_answer"},
    )
    for item in response.output:
        input_items.append(to_input_item(item))
    for item in response.output:
        if item.type == "function_call":
            result = await dispatch(to_input_item(item), channel=channel, mode=mode)
            input_items.append(result.output_item)
            if result.terminal:
                return _finish(_finalize(result.submitted, settings.agent_max_steps, True))

    raise RuntimeError("Forced submit_answer on budget exhaustion failed.")
