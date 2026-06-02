from typing import Literal

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json
from pydantic import BaseModel
from fastapi.responses import StreamingResponse

from app.agent import run_agent
from app.retrieval import aclose

"""
What this file does:
The browser sends one question to POST /query. While the agent works, we want
to show live progress (which searches it runs) and then the final answer. We do
that by streaming events back to the browser as they happen (Server-Sent Events,
SSE) instead of making the browser wait for one big response at the end.

The two helpers that make this work:
1. run_agent is an async function. We start it as its own background task and
   give it an event_sink callback. Every time the agent starts or finishes a
   search, it calls event_sink with a small event dict.
2. A generator task reads those events and sends each one to the browser.

These two tasks pass events to each other through an asyncio.Queue:
   the agent puts events IN, the generator takes them OUT and streams them.
The queue is just a hand-off buffer between "producing" events and "sending"
them, so the agent can keep working while the browser is being fed.

Both tasks run on the same event loop (no threads), so event_sink can put an
event straight into the queue. When the agent is between searches (waiting on
the network), the loop lets the generator run and flush events to the browser.

Order of events the browser receives: one search_start + search_complete pair
per search, then a single answer_complete with the final answer, then the
stream closes.

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
    allow_origins=["http://localhost:3000"],  # Allow browser pages loaded from http://localhost:3000 to call this backend.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# responds to: curl http://localhost:8000/health
@app.get("/health")  # registers function below as HTTP handler: GET request to /health
def health():
    return {"status": "ok"}


@app.on_event("shutdown")
async def _shutdown():
    # Close the async OpenSearch client's aiohttp session on server shutdown.
    await aclose()


# /query endpoint expects JSON shaped like: { "query": "what has the creator said about graph RAG?" }
class QueryRequest(BaseModel):
    query: str
    channel: str = "code4AI"  # default for Phase 1
    mode: Literal["bm25", "dense", "hybrid"] = "hybrid"


def sse(event: dict) -> str:
    """Format a dict as an SSE data line. Note the \n\n, which tells the browser the SSE event is complete."""
    return f"data: {json.dumps(event)}\n\n"


# The function is async because it needs to stream events while other work is happening.
@app.post("/query")
async def query(req: QueryRequest):  # FastAPI automatically turns incoming JSON into a QueryRequest object.
    """
    This code is trying to connect two different worlds:
    - World 1: FastAPI async streaming world
    - World 2: run_agent synchronous/blocking Python world
    Your code needs a bridge between them. That bridge is the `queue`.

    So when the agent says: {"type": "search_start"}
    that event gets placed into the queue.

    Then the streaming generator() takes it out of the queue and yields/sends it to the browser.
    The queue is needed because the agent and the streamer are running in different execution contexts.
    """
    queue: asyncio.Queue = asyncio.Queue()

    def event_sink(event: dict) -> None:
        # run_agent is now awaited directly on this event loop (no worker thread),
        # so emit() runs in the loop thread and can enqueue without the
        # call_soon_threadsafe hop that the old threaded design required.
        queue.put_nowait(event)

    async def run_and_signal():
        """Run the agent to completion, then push the final answer into the queue.

        This runs as its own task so the agent and the streaming generator make
        progress side by side. As the agent runs it calls event_sink, which drops
        search_start / search_complete events into the queue for the generator to
        send. When the agent finishes, we put one answer_complete event in the
        queue. The finally always puts None, the sentinel that tells the generator
        the stream is over (even if the agent raised).
        """
        try:
            result = await run_agent(req.query, req.channel, req.mode, event_sink)
            queue.put_nowait({
                "type": "answer_complete",
                "answer": result.answer,
                "citations": [c.model_dump() for c in result.citations],
            })
        except Exception as e:
            # TECH DEBT: no error event in contract yet; log and close.
            print(f"run_agent raised: {e}")
        finally:
            queue.put_nowait(None)

    async def generator():
        """
        agent produces events → queue → generator → StreamingResponse → browser
        """
        agent_task = asyncio.create_task(run_and_signal())  # Start the agent work, but do not block here waiting for it to finish.
        try:
            while True:
                event = await queue.get()  # Pause here until the queue has an item.
                if event is None:
                    break
                yield sse(event)  # Here, each yield sends one SSE chunk to the browser.
        finally:
            await agent_task

    return StreamingResponse(
        generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache"},
    )