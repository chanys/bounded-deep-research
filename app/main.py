from typing import Literal

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json
from pydantic import BaseModel
from fastapi.responses import StreamingResponse

from app.agent import run_agent
from app.db import transaction
from app.events import AnswerComplete, ErrorEvent
from app.evidence import RunEvidenceState, get_run, latest_run
from app.retrieval import aclose

"""
What this file does:
The browser sends one question to POST /query.
While the agent works, we want to show live progress (which searches it runs) and then the final answer.
We do that by streaming events back to the browser as they happen (Server-Sent Events, SSE)
instead of making the browser wait for one big response at the end.

The two helpers that make this work:
1. run_agent is an async function. We start it as its own background task and give it an event_sink callback.
   Every time the agent does something worth showing, it calls event_sink with a small event dict.
2. A generator task reads those events and sends each one to the browser.

These two tasks pass events to each other through an asyncio.Queue:
  - the agent puts events IN, the generator takes them OUT and streams them.

The queue is just a hand-off buffer between "producing" events and "sending" them,
so the agent can keep working while the browser is being fed.

Both tasks run on the same event loop (no threads), so event_sink can put an event straight into the queue.
When the agent is between steps (waiting on the network), the loop lets the generator run and flush events to the browser.

Order of events on the stream:
- run_started first,
- then for each turn a turn_start / turn_complete pair around the model call,
- with search_start / search_complete and read_start / read_complete for the tool calls in between.
- A successful run ends with answer_complete; a failed one ends with error.

Either way the stream then closes.
The folded run summary is not on the stream; it is fetched afterward from the separate GET /runs/{run_id}/evidence endpoint.

Call chain:
    Browser
      -> POST /query
        -> StreamingResponse
          -> generator()        (reads from queue, sends SSE to browser)
            -> run_and_signal() (runs the agent, puts events in the queue)
              -> run_agent(...)
"""

app = FastAPI(title="bounded-deep-research")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # let the frontend dev server (port 3000) call this backend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    """Liveness check. `curl http://localhost:8000/health` returns {"status": "ok"}."""
    return {"status": "ok"}


@app.on_event("shutdown")
async def _shutdown():
    """On server shutdown, close the async OpenSearch client's aiohttp session so
    it doesn't leak / warn at exit."""
    await aclose()


# Read-only endpoints for the Run Audit panel. Each returns a stored
# RunEvidenceState exactly as it was saved, without adding anything to it.
#
# Why the order of these two routes matters:
# {run_id} is a wildcard that matches ANY path segment, including the literal word "latest".
# So the URL /runs/latest/evidence matches BOTH routes below.
# FastAPI does not pick the more specific route; it uses the first route that matches, in declaration order.
# So /runs/latest/evidence must come first.
# If /runs/{run_id}/evidence came first, a request for "latest" would hit it with run_id="latest",
# look up a run with that id, find none, and 404.
# A real run id (not the word "latest") doesn't match the first route, so it correctly falls through to the {run_id} route.
@app.get("/runs/latest/evidence", response_model=RunEvidenceState)
def latest_evidence():
    """Return the evidence for the most recently finished run (for the demo's Run Audit panel).
    404 if no run has completed yet."""
    state = latest_run()
    if state is None:
        raise HTTPException(status_code=404, detail="no runs recorded yet")
    return state


@app.get("/runs/{run_id}/evidence", response_model=RunEvidenceState)
def run_evidence(run_id: str):
    """Return the evidence for a specific run by id (the run_id from the
    run_started event). 404 if there is no such run."""
    state = get_run(run_id)
    if state is None:
        raise HTTPException(status_code=404, detail=f"unknown run_id: {run_id}")
    return state


class HydrateRequest(BaseModel):
    """JSON body of a POST /citations/hydrate request: the video ids to look up."""

    video_ids: list[str]


@app.post("/citations/hydrate")
def hydrate_citations(req: HydrateRequest) -> dict[str, str]:
    """Resolve video ids to titles in one batch query (no YouTube API call).

    Citations arrive as ids only; the frontend calls this once to get titles for
    the citation cards. Thumbnails and deep links are derived from the id on the
    client, so titles are the only thing that needs a lookup. Returns a
    {video_id: title} map; ids with no row are simply absent.
    """
    if not req.video_ids:
        return {}
    with transaction() as conn:
        rows = conn.execute(
            "SELECT video_id, title FROM videos WHERE video_id = ANY(%s)",
            (req.video_ids,),
        ).fetchall()
    return {r["video_id"]: r["title"] for r in rows}


class QueryRequest(BaseModel):
    """JSON body of a POST /query request."""

    query: str                  # the user's question
    channel: str = "code4AI"    # which corpus to search (one channel for now)
    mode: Literal["bm25", "dense", "hybrid"] = "hybrid"   # retrieval strategy


def sse(event: dict) -> str:
    """Format one event dict as an SSE record: a `data:` line followed by a blank
    line. The blank line is what tells the browser the event is complete."""
    return f"data: {json.dumps(event)}\n\n"


@app.post("/query")
async def query(req: QueryRequest):   # FastAPI parses the JSON body into a QueryRequest
    """Run the agent for one query and stream its progress back as SSE.

    The endpoint is async because it has to keep sending events while the agent is
    still working. It bridges two concurrent tasks with an asyncio.Queue: the
    agent (in run_and_signal) produces events into the queue, and the generator
    drains the queue and writes them to the response.
    """
    queue: asyncio.Queue = asyncio.Queue()

    def event_sink(event: dict) -> None:
        """Hand one agent event to the stream. run_agent is awaited on this same
        event loop (no worker thread), so we can enqueue directly without the
        call_soon_threadsafe hop the old threaded design needed."""
        queue.put_nowait(event)

    async def run_and_signal():
        """Run the agent to completion, then push the final result onto the queue.

        Runs as its own task so the agent and the streaming generator make progress
        side by side. While running, the agent calls event_sink, dropping progress
        events into the queue for the generator to send. On success we enqueue one
        answer_complete; on failure, one error. The finally always enqueues None,
        the sentinel that tells the generator the stream is over.
        """
        try:
            result = await run_agent(req.query, req.channel, req.mode, event_sink)
            queue.put_nowait(AnswerComplete(
                answer=result.answer,
                citations=[c.model_dump() for c in result.citations],
            ).model_dump())
        except Exception as e:
            queue.put_nowait(ErrorEvent(message=f"{type(e).__name__}: {e}").model_dump())
        finally:
            queue.put_nowait(None)

    async def generator():
        """Drain the queue and yield each event as an SSE record, until the None
        sentinel. The flow is: agent -> queue -> generator -> StreamingResponse ->
        browser."""
        # Start the agent in the background; do not block here waiting for it.
        agent_task = asyncio.create_task(run_and_signal())
        try:
            while True:
                event = await queue.get()   # wait until the next event is available
                if event is None:           # sentinel: the run is done
                    break
                yield sse(event)            # send one SSE record to the browser
        finally:
            await agent_task                # ensure the agent task is awaited/cleaned up

    return StreamingResponse(
        generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache"},
    )
