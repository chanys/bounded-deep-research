"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import ReactMarkdown from "react-markdown";
import { TracePanel, type TraceItem } from "@/components/TracePanel";
import { CitationCard } from "@/components/CitationCard";
import type { Citation, SseEvent } from "@/lib/events";
import { streamQuery } from "@/lib/sse";
import { hydrateCitations } from "@/lib/api";

// One-click examples spanning the recipe's tiers (factual / comparative / longitudinal).
const EXAMPLE_PROMPTS = [
  "What two techniques does Llama 4 Scout use to achieve its 10 million token context length?",
  "How does the creator distinguish RAG from the broader 'AI harness', and what role does each play?",
  "How has the creator's view of LLM reasoning evolved over 2025-2026?",
];

export default function QueryPage() {
  const [query, setQuery] = useState("");
  const [isRunning, setIsRunning] = useState(false);
  const [runId, setRunId] = useState<string | null>(null);
  const [trace, setTrace] = useState<TraceItem[]>([]);
  const [thinking, setThinking] = useState(false);
  const [tokens, setTokens] = useState(0);
  const [elapsedMs, setElapsedMs] = useState(0);
  const [answerText, setAnswerText] = useState(""); // grows from answer_delta, finalized by answer_complete
  const [citations, setCitations] = useState<Citation[]>([]);
  const [titles, setTitles] = useState<Record<string, string>>({}); // video_id -> title
  const [error, setError] = useState<string | null>(null);

  // Elapsed-time clock: ticks while a run is in flight, freezes when it ends.
  useEffect(() => {
    if (!isRunning) return;
    const start = performance.now();
    const id = setInterval(() => setElapsedMs(performance.now() - start), 1000);
    return () => clearInterval(id);
  }, [isRunning]);

  const handleEvent = (event: SseEvent) => {
    // Discriminated union: TypeScript narrows `event` inside each branch.
    switch (event.type) {
      case "run_started":
        setRunId(event.run_id); // stashed for the Day-5 Run Audit fetch
        break;

      // Model turn lifecycle drives the token-in-flight indicator.
      case "turn_start":
        setThinking(true);
        break;
      case "turn_complete":
        setThinking(false);
        setTokens((t) => t + event.usage.total_tokens);
        break;

      // Searches: append on start, fill result count on complete (by search_id).
      case "search_start":
        setTrace((prev) => [
          ...prev,
          { kind: "search", id: event.search_id, query: event.query, resultCount: null },
        ]);
        break;
      case "search_complete":
        setTrace((prev) =>
          prev.map((it) =>
            it.kind === "search" && it.id === event.search_id
              ? { ...it, resultCount: event.result_count }
              : it,
          ),
        );
        break;

      // Reads: append on start, set status on complete (by read_id).
      case "read_start":
        setTrace((prev) => [
          ...prev,
          {
            kind: "read",
            id: event.read_id,
            videoId: event.video_id,
            startTs: event.start_ts,
            status: "reading",
          },
        ]);
        break;
      case "read_complete":
        setTrace((prev) =>
          prev.map((it) =>
            it.kind === "read" && it.id === event.read_id
              ? { ...it, status: event.ok ? "ok" : "not_found" }
              : it,
          ),
        );
        break;

      // Answer streams in piece by piece, then answer_complete delivers the
      // authoritative final text + citations. We then fetch the citation titles.
      case "answer_delta":
        setAnswerText((prev) => prev + event.text);
        break;
      case "answer_complete":
        setAnswerText(event.answer);
        setCitations(event.citations);
        {
          const ids = [...new Set(event.citations.map((c) => c.video_id))];
          hydrateCitations(ids).then(setTitles);
        }
        break;
      case "error":
        setError(event.message);
        break;
      default:
        break;
    }
  };

  const runQuery = async (q: string) => {
    if (!q.trim() || isRunning) return;

    // Reset state for a new run.
    setIsRunning(true);
    setRunId(null);
    setTrace([]);
    setThinking(false);
    setTokens(0);
    setElapsedMs(0);
    setAnswerText("");
    setCitations([]);
    setTitles({});
    setError(null);

    try {
      for await (const event of streamQuery({ query: q })) {
        handleEvent(event);
      }
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      setIsRunning(false);
      setThinking(false);
    }
  };

  return (
    <main className="max-w-3xl mx-auto p-8 font-sans">
      <div className="mb-6 flex items-baseline justify-between">
        <h1 className="text-2xl font-semibold">Bounded Deep Research</h1>
        <Link href="/system" className="text-sm text-zinc-500 underline">
          system →
        </Link>
      </div>

      <div className="mb-4">
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
          onClick={() => runQuery(query)}
          disabled={isRunning || !query.trim()}
        >
          {isRunning ? "Running..." : "Ask"}
        </button>
      </div>

      <div className="mb-8 flex flex-wrap gap-2">
        {EXAMPLE_PROMPTS.map((p) => (
          <button
            key={p}
            className="text-xs text-left px-3 py-1.5 border border-zinc-200 rounded-full text-zinc-600 hover:bg-zinc-50 disabled:opacity-50"
            onClick={() => {
              setQuery(p);
              runQuery(p);
            }}
            disabled={isRunning}
          >
            {p.length > 60 ? p.slice(0, 60) + "…" : p}
          </button>
        ))}
      </div>

      {runId && (
        <p className="mb-4 text-xs font-mono text-zinc-400">run: {runId}</p>
      )}

      {error && (
        <div className="mb-6 p-3 bg-red-50 text-red-800 rounded">
          Error: {error}
        </div>
      )}

      <TracePanel
        trace={trace}
        thinking={thinking}
        tokens={tokens}
        elapsedMs={elapsedMs}
        isRunning={isRunning}
      />

      {answerText && (
        <div className="mb-8">
          <h2 className="text-sm font-semibold text-zinc-600 mb-2">Answer</h2>
          <div className="markdown-answer">
            <ReactMarkdown>{answerText}</ReactMarkdown>
          </div>

          {citations.length > 0 && (
            <>
              <h2 className="text-sm font-semibold text-zinc-600 mt-6 mb-2">
                Citations
              </h2>
              <div className="grid gap-2 sm:grid-cols-2">
                {citations.map((c, i) => (
                  <CitationCard
                    key={i}
                    citation={c}
                    title={titles[c.video_id]}
                  />
                ))}
              </div>
            </>
          )}
        </div>
      )}
    </main>
  );
}
