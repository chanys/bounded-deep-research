"use client";

import { useState } from "react";

// Mirrors the SSE event contract in planning_docs/day-4-sse-contract.md.
type SearchStart = { type: "search_start"; search_id: number; query: string };
type SearchComplete = { type: "search_complete"; search_id: number; result_count: number };
type AnswerComplete = {
  type: "answer_complete";
  answer: string;
  citations: { video_id: string; start_ts: number; end_ts: number }[];
};
type SseEvent = SearchStart | SearchComplete | AnswerComplete;

// One row in the trace panel — the UI's view of a single search.
// search_id is the correlation key with the SSE events.
type SearchRow = {
  search_id: number;
  query: string;
  result_count: number | null; // null = in-flight
};

export default function QueryPage() {
  const [query, setQuery] = useState("");
  const [isRunning, setIsRunning] = useState(false);
  const [searches, setSearches] = useState<SearchRow[]>([]);
  const [answer, setAnswer] = useState<AnswerComplete | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async () => {
    if (!query.trim() || isRunning) return;

    // Reset state for a new run.
    setIsRunning(true);
    setSearches([]);
    setAnswer(null);
    setError(null);

    try {
      const response = await fetch("http://localhost:8000/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });

      if (!response.ok || !response.body) {
        throw new Error(`Request failed: ${response.status}`);
      }

      // Parse the SSE stream manually. EventSource doesn't support POST,
      // so we use fetch + a ReadableStream reader and split on "\n\n".
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });

        // SSE events are separated by a blank line (\n\n).
        const parts = buffer.split("\n\n");
        buffer = parts.pop() ?? ""; // keep the last, possibly-incomplete chunk

        for (const part of parts) {
          if (!part.startsWith("data: ")) continue;
          const json = part.slice("data: ".length);
          const event = JSON.parse(json) as SseEvent;
          handleEvent(event);
        }
      }
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      setIsRunning(false);
    }
  };

  const handleEvent = (event: SseEvent) => {
    if (event.type === "search_start") {
      setSearches((prev) => [
        ...prev,
        { search_id: event.search_id, query: event.query, result_count: null },
      ]);
    } else if (event.type === "search_complete") {
      setSearches((prev) =>
        prev.map((s) =>
          s.search_id === event.search_id
            ? { ...s, result_count: event.result_count }
            : s
        )
      );
    } else if (event.type === "answer_complete") {
      setAnswer(event);
    }
  };

  return (
    <main className="max-w-3xl mx-auto p-8 font-sans">
      <h1 className="text-2xl font-semibold mb-6">Bounded Deep Research</h1>

      <div className="mb-8">
        <textarea
          className="w-full p-3 border border-zinc-300 rounded"
          rows={3}
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask a question about the Discover AI corpus..."
          disabled={isRunning}
        />
        <button
          className="mt-2 px-4 py-2 bg-black text-white rounded disabled:bg-zinc-400"
          onClick={handleSubmit}
          disabled={isRunning || !query.trim()}
        >
          {isRunning ? "Running..." : "Ask"}
        </button>
      </div>

      {error && (
        <div className="mb-6 p-3 bg-red-50 text-red-800 rounded">
          Error: {error}
        </div>
      )}

      {searches.length > 0 && (
        <div className="mb-8">
          <h2 className="text-sm font-semibold text-zinc-600 mb-2">Trace</h2>
          <ul className="space-y-1 text-sm font-mono">
            {searches.map((s) => (
              <li key={s.search_id}>
                [{s.search_id}] search: {s.query}
                {s.result_count === null
                  ? " — searching..."
                  : ` — ${s.result_count} results`}
              </li>
            ))}
          </ul>
        </div>
      )}

      {answer && (
        <div className="mb-8">
          <h2 className="text-sm font-semibold text-zinc-600 mb-2">Answer</h2>
          <div className="whitespace-pre-wrap">{answer.answer}</div>

          <h2 className="text-sm font-semibold text-zinc-600 mt-6 mb-2">
            Citations
          </h2>
          <ul className="space-y-1 text-sm font-mono">
              {answer.citations.map((c, i) => (
                <li key={i}>
                  <a
                    href={`https://www.youtube.com/watch?v=${c.video_id}&t=${c.start_ts}s`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="underline"
                  >
                    {c.video_id} @ {c.start_ts}–{c.end_ts}
                  </a>
                </li>
              ))}
            </ul>

        </div>
      )}
    </main>
  );
}