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
import re
from uuid import uuid4

from langfuse import observe, get_client

from app.config import settings
from app.evidence import EvidenceCollector, put_run
from app.events import (
    RunStarted, TurnStart, TurnComplete,
    SearchStart, SearchComplete, ReadStart, ReadComplete, AnswerDelta, usage_dict,
)
from app.llm import respond, to_input_item
from app.prompts import load_recipe
from app.retrieval import Mode
from app.tools import EXPLORE_TOOLS, SUBMIT_TOOLS, dispatch, SubmittedAnswer


_RECIPE_METADATA, SYSTEM_PROMPT = load_recipe()


def _noop(event: dict) -> None:
    """Default event sink: silently drops events when no caller is listening."""


class _AnswerStream:
    """Pulls the final answer text out of submit_answer's streamed arguments.

    submit_answer's arguments arrive over the stream as a growing JSON string,
    like {"answer":"...so far...","citations":[...]}. This watches for the
    "answer" field and decodes its string value as it grows, returning only the
    newly added text on each feed() so the UI can append it.

    It re-decodes the value from the field start every time rather than tracking
    escape state across delta boundaries, which keeps backslash escapes correct
    even when a delta splits one. (\\uXXXX escapes are not decoded; the model
    effectively never emits them in answer prose.)
    """

    _KEY = re.compile(r'"answer"\s*:\s*"')
    _UNESCAPE = {"n": "\n", "t": "\t", "r": "\r", '"': '"', "\\": "\\", "/": "/", "b": "\b", "f": "\f"}

    def __init__(self):
        self._buf = ""           # all argument text seen so far
        self._value_start = -1   # index just past the answer value's opening quote
        self._emitted = 0        # count of decoded chars already returned
        self._done = False       # True once the value's closing quote is seen

    def feed(self, delta: str) -> str:
        """Add one argument-delta chunk and return any newly decoded answer text."""
        if self._done:
            return ""
        self._buf += delta
        if self._value_start < 0:
            m = self._KEY.search(self._buf)
            if not m:
                return ""        # the "answer" field hasn't started yet
            self._value_start = m.end()

        # Decode the JSON string value until an unescaped closing quote.
        decoded: list[str] = []
        esc = False
        i = self._value_start
        ended = False
        while i < len(self._buf):
            c = self._buf[i]
            if esc:
                decoded.append(self._UNESCAPE.get(c, c))
                esc = False
            elif c == "\\":
                esc = True
            elif c == '"':
                ended = True
                break
            else:
                decoded.append(c)
            i += 1

        text = "".join(decoded)
        new = text[self._emitted:]   # only the part we haven't emitted yet
        self._emitted = len(text)
        if ended:
            self._done = True
        return new


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
                    recipe_version=_RECIPE_METADATA.version,
                    max_steps=settings.agent_max_steps).model_dump())

    # Counters for the per-search and per-read ids. They span the whole run and
    # are handed out in a sync pre-pass (below) before the parallel dispatch, so
    # an id is fixed before its coroutine starts, regardless of finish order.
    search_id_counter = 0
    read_id_counter = 0

    async def _respond_turn(step, tools, tool_choice, effort=None, stream_answer=True):
        """Run one model call (one "turn") and bracket it with two events:
        turn_start just before, and turn_complete just after (the latter carries
        this call's token usage, for the UI counter and the cost fold).

        Parameters:
          tools:  which tools the model may call this turn. Exploration turns pass
                  EXPLORE_TOOLS (search / read / mark_ready); synthesis passes
                  SUBMIT_TOOLS (submit_answer only, forced via tool_choice).
          effort: reasoning-effort override for this call. Exploration runs at the
                  global `none`; synthesis runs at `synthesis_reasoning_effort`.
          stream_answer: whether to stream the submit_answer text to the UI as it
                  is written. Only the synthesis turn writes an answer, so only it
                  streams; exploration turns pass False and run non-streaming.
        """
        emit(TurnStart(step=step).model_dump())

        on_event = None
        if stream_answer:
            extractor = _AnswerStream()   # turns raw argument JSON chunks into answer text
            submit_index = None           # which output slot the submit_answer call is in

            def on_event(ev):  # noqa: F811 (reassigns the on_event = None default above)
                """Stream the answer to the UI as the model writes it.

                Runs only on the synthesis turn (the only one with stream_answer),
                which is forced to call submit_answer. The streaming protocol
                delivers a function call's arguments in two steps: an
                `output_item.added` event announces the submit_answer call and its
                output slot, then `function_call_arguments.delta` events carry the
                arguments JSON in chunks. So we note that slot, feed its chunks to
                the extractor (which pulls out the newly written "answer" text), and
                emit each new piece as an answer_delta. The slot check is defensive;
                this turn only ever has the one submit_answer call.
                """
                nonlocal submit_index
                et = getattr(ev, "type", None)
                if et == "response.output_item.added":
                    item = ev.item
                    if getattr(item, "type", None) == "function_call" and getattr(item, "name", None) == "submit_answer":
                        submit_index = ev.output_index
                elif et == "response.function_call_arguments.delta":
                    if submit_index is not None and ev.output_index == submit_index:
                        piece = extractor.feed(ev.delta)
                        if piece:
                            emit(AnswerDelta(text=piece).model_dump())

        response = await respond(input_items, tools=tools, tool_choice=tool_choice,
                                 on_event=on_event, effort=effort)
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

    async def _synthesize(steps_used: int, budget_exhausted: bool) -> AgentResult:
        """Produce the final answer as a dedicated forced submit_answer turn, run at
        `synthesis_reasoning_effort` (low) rather than the exploration effort (none).
        This is the only turn whose answer is streamed to the UI."""
        response = await _respond_turn(
            steps_used,
            tools=SUBMIT_TOOLS,
            tool_choice={"type": "function", "name": "submit_answer"},
            effort=settings.synthesis_reasoning_effort,
            stream_answer=True,
        )
        for item in response.output:
            input_items.append(to_input_item(item))
        for item in response.output:
            if item.type == "function_call":
                result = await dispatch(to_input_item(item), channel=channel, mode=mode)
                input_items.append(result.output_item)
                if result.terminal:
                    return _finalize(result.submitted, steps_used, budget_exhausted)
        raise RuntimeError("Forced submit_answer synthesis failed.")

    for step in range(settings.agent_max_steps):
        # Exploration turn: search/read/mark_ready at the global effort (no answer
        # is generated here, and nothing is streamed).
        response = await _respond_turn(step, tools=EXPLORE_TOOLS, tool_choice="required",
                                       stream_answer=False)

        # Append reasoning/messages and search/read calls. A mark_ready call is the
        # model's "ready" signal: skip it (no args, no answer, nothing wasted) and
        # synthesize below at the synthesis effort.
        ready = False
        for item in response.output:
            if item.type == "function_call" and item.name == "mark_ready":
                ready = True
                continue
            input_items.append(to_input_item(item))

        # Collect this turn's search/read calls and assign ids in a sync pre-pass,
        # so ids are fixed before the parallel dispatch.
        call_items = [
            to_input_item(item)
            for item in response.output
            if item.type == "function_call" and item.name != "mark_ready"
        ]
        slots: list[tuple[str, int]] = []
        for call_item in call_items:
            if call_item["name"] == "search_transcripts":
                slots.append(("search", search_id_counter))
                search_id_counter += 1
            else:  # read_video_segment
                slots.append(("read", read_id_counter))
                read_id_counter += 1

        results = await asyncio.gather(*(
            _dispatch_with_events(call_item, kind, ev_id)
            for call_item, (kind, ev_id) in zip(call_items, slots)
        ))
        for result in results:
            input_items.append(result.output_item)

        # Model signaled ready -> synthesize the final answer at the synthesis effort.
        if ready:
            return _finish(await _synthesize(step + 1, budget_exhausted=False))

        # No tool call at all is unexpected, since tool_choice is "required".
        if not call_items:
            raise RuntimeError(
                f"Agent emitted no tool call at step {step + 1}. "
                f"Output: {response.output_text!r}"
            )

    # Step budget exhausted without the model signaling ready: force synthesis now.
    input_items.append({
        "role": "user",
        "content": (
            "Step budget exhausted. Submit your best answer now from the evidence "
            "gathered so far; if evidence is insufficient, say so in the answer."
        ),
    })
    return _finish(await _synthesize(settings.agent_max_steps, budget_exhausted=True))
