from contextlib import asynccontextmanager
from typing import Literal

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json
from pydantic import BaseModel
from fastapi.responses import StreamingResponse

from app import limits
from app.agent import run_agent
from app.channels import CHANNELS
from core.config import settings
from core.db import transaction
from app.events import AnswerComplete, ErrorEvent
from app.evidence import RunEvidenceState, get_run, latest_run, take_partial_cost
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
- with search_start / search_complete for the searches in between.
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

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup/shutdown hook (the modern replacement for @app.on_event). Code before
    `yield` runs on startup, code after runs on shutdown, e.g. when AWS stops the
    container. We close the OpenSearch client here; it's a no-op under the pgvector
    backend, where no client was ever opened."""
    limits.ensure_tables()  # make sure the daily_spend table exists before serving
    yield
    await aclose()


app = FastAPI(title="bounded-deep-research", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins,  # from env; localhost in dev, app domain in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    """Liveness check. `curl http://localhost:8000/health` returns {"status": "ok"}."""
    return {"status": "ok"}


@app.get("/channels")
def channels() -> list[dict]:
    """The channel registry, in display order, for the UI's channel picker.

    `output_directive` is a prompt-engineering detail, so it stays server-side.
    """
    return [c.model_dump(exclude={"output_directive"}) for c in CHANNELS.values()]


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
    channel: str = "code4AI"    # which corpus to search; must be a key of app.channels.CHANNELS
    mode: Literal["bm25", "dense", "hybrid"] = "hybrid"   # retrieval strategy
    access_code: str | None = None  # a valid one unlocks the higher quota


def sse(event: dict) -> str:
    """Format one event dict as an SSE record: a `data:` line followed by a blank
    line. The blank line is what tells the browser the event is complete."""
    return f"data: {json.dumps(event)}\n\n"


@app.post("/query")
async def query(req: QueryRequest, request: Request):   # FastAPI parses the JSON body into a QueryRequest
    """Run the agent for one query and stream its progress back as SSE.

    The endpoint is async because it has to keep sending events while the agent is
    still working. It bridges two concurrent tasks with an asyncio.Queue: the
    agent (in run_and_signal) produces events into the queue, and the generator
    drains the queue and writes them to the response.
    """
    # A one-event SSE error stream, used for the gate rejections below. The frontend
    # renders these like any other error.
    def error_stream(message: str) -> StreamingResponse:
        async def gen():
            yield sse(ErrorEvent(message=message).model_dump())
        return StreamingResponse(gen(), media_type="text/event-stream",
                                 headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})

    # Gate 0 - the channel must exist in the registry. Checked before the paid gates:
    # an unknown channel would silently search an empty corpus and still burn budget.
    if req.channel not in CHANNELS:
        return error_stream(f"Unknown channel: {req.channel}")

    # Determine the tier from the supplied code (the private owner code wins over the
    # shared access code). Each tier draws on a budget bucket with its own daily cap.
    code = req.access_code
    if settings.owner_code and code == settings.owner_code:
        tier, bucket, cap = "owner", "owner", settings.owner_spend_cap_usd
    elif settings.access_code and code == settings.access_code:
        tier, bucket, cap = "coded", "public", settings.daily_spend_cap_usd
    else:
        tier, bucket, cap = "anon", "public", settings.daily_spend_cap_usd

    # Gate 1 - spend breaker for this tier's budget, before any paid work.
    if await asyncio.to_thread(limits.over_cap, bucket, cap):
        return error_stream("The demo's daily usage limit has been reached. Please try again tomorrow.")

    # Gate 2 - per-IP daily quota (the owner code is exempt). Behind the load balancer the
    # real client IP is the first entry of X-Forwarded-For.
    if tier != "owner":
        limit = settings.coded_daily_quota if tier == "coded" else settings.anon_daily_quota
        xff = request.headers.get("x-forwarded-for")
        client_ip = xff.split(",")[0].strip() if xff else (request.client.host if request.client else "unknown")
        if not await asyncio.to_thread(limits.check_and_count, client_ip, limit):
            hint = "" if tier == "coded" else " Enter the access code for a higher limit."
            return error_stream(f"You've reached today's query limit.{hint}")

    queue: asyncio.Queue = asyncio.Queue()
    run_id: str | None = None  # captured from run_started, used to record this run's cost

    def event_sink(event: dict) -> None:
        """Hand one agent event to the stream. run_agent is awaited on this same
        event loop (no worker thread), so we can enqueue directly without the
        call_soon_threadsafe hop the old threaded design needed."""
        nonlocal run_id
        if event.get("type") == "run_started":
            run_id = event.get("run_id")
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
            # Record this run's cost against today's spend for the right budget bucket.
            evidence = get_run(run_id) if run_id else latest_run()
            if evidence is not None:
                await asyncio.to_thread(limits.add_spend, bucket, evidence.usd_cost)
        except Exception as e:
            queue.put_nowait(ErrorEvent(message=f"{type(e).__name__}: {e}").model_dump())
            # A run that raised never recorded its cost, so charge whatever it spent
            # before dying against today's budget; without this the breaker undercounts
            # exactly the failed runs that burned tokens. Zero if it died before any
            # model call. run_id is None only if run_started never fired.
            if run_id:
                partial = take_partial_cost(run_id)
                if partial > 0:
                    await asyncio.to_thread(limits.add_spend, bucket, partial)
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
                # Heartbeat: if no event arrives within 15s (e.g. the quiet synthesis
                # turn), send an SSE comment line. The browser ignores it, but it keeps
                # the connection alive so the load balancer's idle timeout never fires.
                try:
                    event = await asyncio.wait_for(queue.get(), timeout=15)
                except asyncio.TimeoutError:
                    yield ": keepalive\n\n"
                    continue
                if event is None:           # sentinel: the run is done
                    break
                yield sse(event)            # send one SSE record to the browser
        finally:
            await agent_task                # ensure the agent task is awaited/cleaned up

    return StreamingResponse(
        generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
