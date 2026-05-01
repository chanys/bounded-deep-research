from typing import Literal

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json
from pydantic import BaseModel
from fastapi.responses import StreamingResponse

from app.agent import run_agent

"""
**Pattern for this main.py:**
“I implemented an SSE-based streaming interface for a blocking agent by bridging a worker thread into an async FastAPI endpoint using an asyncio queue.”

Browser / frontend
        |
        | POST /query
        v
FastAPI endpoint in main.py
        |
        | calls run_agent(...)
        v
Agent code
        |
        | emits progress events
        v
main.py turns events into SSE stream
        |
        v
Browser receives progress + final answer

----------------------------------------------------

uvicorn is the server process
FastAPI is the app
`/query` is an async endpoint running inside uvicorn's event loop

In this code, we run `run_agent(...)` in a background thread so the 
FastAPI `/query` endpoint can keep streaming events instead of freezing.

-----------------------------------------------------

The Whole Flow:
```
Browser              FastAPI async endpoint          Agent thread
   |                         |                            |
   |--- POST /query -------->|                            |
   |                         | create queue               |
   |                         | get event loop             |
   |                         | start generator            |
   |                         | start run_agent in thread -|
   |                         |                            |
   |                         |<--- event_sink(event) -----|
   |                         | put event into queue       |
   |<-- SSE event -----------|                            |
   |                         |                            |
```

Imagine a restaurant.
- The agent thread is the kitchen.
- The browser stream is the waiter serving the customer.
- The queue is the pickup counter.
- The event loop is the floor manager.

But because the kitchen and waiter are working in different “threads,”
the kitchen does not shove things directly into the waiter’s hands.
It asks the floor manager to place it properly on the counter.

------------------------------------

The call chain is roughly:
```
Browser
  → FastAPI /query
    → StreamingResponse
      → generator()
        → run_and_signal()
          → run_agent(...)
```

The event flow is:          
```
run_agent emits event
      ↓
event_sink receives event
      ↓
event goes into queue
      ↓
generator gets event from queue
      ↓
generator converts event to SSE format
      ↓
StreamingResponse sends it to browser
```

The whole flow in one sequence:
```
Browser                  FastAPI /query                 Agent thread
   |                           |                              |
   |--- POST /query ---------->|                              |
   |                           | create queue                 |
   |                           | return StreamingResponse     |
   |                           |                              |
   |                           | generator starts             |
   |                           | create run_and_signal task   |
   |                           |                              |
   |                           | run_agent in thread -------->|
   |                           |                              |
   |                           |<--- event_sink(search_start)-|
   |                           | put event in queue           |
   |<-- SSE search_start ------|                              |
   |                           |                              |
   |                           |<--- event_sink(search_done)--|
   |                           | put event in queue           |
   |<-- SSE search_complete ---|                              |
   |                           |                              |
   |                           |<--- AgentResult -------------|
   |                           | put answer_complete in queue |
   |<-- SSE answer_complete ---|                              |
   |                           | put None in queue            |
   |                           | generator stops              |
   |                           | stream closes                |
```

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

    # This grabs the current asyncio event loop.
    # The event loop is the thing managing async tasks inside your FastAPI endpoint.
    # So loop is a handle to the async world.
    loop = asyncio.get_running_loop()

    def event_sink(event: dict) -> None:
        # Called from the agent thread. Use call_soon_threadsafe to hop back to the event loop.
        # This means: "Hey event loop, safely run queue.put_nowait(event) from your own thread."
        # So the agent thread does not directly touch the queue. It asks the event loop to do it safely.
        #
        # `run_agent` is running in a background thread, while `queue` belongs to the asyncio event loop thread
        # `call_soon_threadsafe` means: As soon as you can, safely put this event into the queue from the event loop thread.
        # So the following line safely moves an event from the agent thread into the async streaming pipeline.
        loop.call_soon_threadsafe(queue.put_nowait, event)

    async def run_and_signal():
        """
        Notice that the `/query` function is async

        But the agent is normal blocking code: `run_agent(req.query, event_sink)`
        `run_agent` may take 10–15 seconds.
        If we called it directly: `result = run_agent(req.query, event_sink)`
        then the endpoint would be stuck until the agent finishes.
        The server could not stream intermediate events smoothly because the /query function is busy waiting for `run_agent` to return.

        So instead we do: `result = await asyncio.to_thread(run_agent, req.query, event_sink)`
        which means: Run the blocking agent in a separate thread, while the async /query endpoint continues managing the stream.
        """
        try:
            result = await asyncio.to_thread(run_agent, req.query, req.channel, req.mode, event_sink)
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