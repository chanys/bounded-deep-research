// Typed client for the /query SSE stream.
//
// EventSource doesn't support POST, so we read the response body as a stream and
// split on the SSE record separator ("\n\n"). Exposed as an async generator so a
// component can simply `for await (const event of streamQuery(req))`.

import type { SseEvent } from "./events";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8000";

export type QueryRequest = {
  query: string;
  channel?: string;
  mode?: "bm25" | "dense" | "hybrid";
};

export async function* streamQuery(
  req: QueryRequest,
  signal?: AbortSignal,
): AsyncGenerator<SseEvent> {
  const res = await fetch(`${API_BASE}/query`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(req),
    signal,
  });

  if (!res.ok || !res.body) {
    throw new Error(`Request failed: ${res.status}`);
  }

  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });

    // SSE records are separated by a blank line. Keep the last, possibly
    // incomplete, chunk in the buffer for the next read.
    const parts = buffer.split("\n\n");
    buffer = parts.pop() ?? "";

    for (const part of parts) {
      const line = part.trim();
      if (!line.startsWith("data:")) continue;
      const json = line.slice(line.indexOf(":") + 1).trim();
      yield JSON.parse(json) as SseEvent;
    }
  }
}
