"use client";

import { useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";
import { TracePanel, type TraceItem } from "@/components/TracePanel";
import { Sources } from "@/components/Sources";
import { VerificationStrip } from "@/components/VerificationStrip";
import type { Citation, SseEvent } from "@/lib/events";
import { streamQuery } from "@/lib/sse";
import { hydrateCitations, fetchLatestEvidence, type RunEvidence } from "@/lib/api";

// The model marks citations inline, but the exact form varies: either
// (video_id, start, end) tuples or [start-end] timestamp ranges (any dash). We
// rewrite each marker that maps to a known citation into a markdown link
// [n](#source-n), which renders as a numbered chip linking to its Sources row.
// Mapping is by (video_id, start) for tuples and by (start, end) for ranges. A
// bracket range that doesn't match a real citation (e.g. a year range like
// [2025-2026]) is left untouched, as are all markers during streaming (before
// citations are known).
function withCitationChips(text: string, citations: Citation[]): string {
  if (citations.length === 0) return text;
  const byVidStart = new Map<string, number>();
  const byRange = new Map<string, number>();
  citations.forEach((c, i) => {
    byVidStart.set(`${c.video_id}:${c.start_ts}`, i + 1);
    byRange.set(`${c.start_ts}-${c.end_ts}`, i + 1);
  });

  return text
    // (video_id, start, end)
    .replace(/\(([A-Za-z0-9_-]+),\s*(\d+),\s*(\d+)\)/g, (whole, vid, start) => {
      const n = byVidStart.get(`${vid}:${start}`);
      return n ? `[${n}](#source-${n})` : whole;
    })
    // [start-end] with a hyphen, en-dash, or em-dash; possibly chained
    .replace(/\[(\d+)\s*[-–—]\s*(\d+)\]/g, (whole, start, end) => {
      const n = byRange.get(`${start}-${end}`);
      return n ? `[${n}](#source-${n})` : whole;
    });
}

// One-click examples: a comparative question and a longitudinal one (two, so they
// sit as one balanced row).
const EXAMPLE_PROMPTS = [
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
  const [maxSteps, setMaxSteps] = useState<number | null>(null); // step budget from run_started
  const [evidence, setEvidence] = useState<RunEvidence | null>(null); // fetched after the run
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
        setRunId(event.run_id); // stashed for the Run Audit fetch
        setMaxSteps(event.max_steps);
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
              ? { ...it, status: event.ok ? "ok" : "not_found", endTs: event.end_ts }
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
        // Evidence is stored server-side before answer_complete is emitted, so the
        // just-finished run is the latest. Fetch it for the verification strip.
        fetchLatestEvidence().then(setEvidence);
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
    setMaxSteps(null);
    setEvidence(null);
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

  const started = isRunning || !!answerText || trace.length > 0;

  return (
    <main className="mx-auto max-w-5xl px-6 py-8">
      {/* Ask box: borderless textarea on a raised card surface. */}
      <div className="rounded-xl border border-border bg-card p-4 shadow-sm">
        <textarea
          className="w-full resize-none bg-transparent text-[15px] outline-none placeholder:text-muted-foreground"
          rows={3}
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask a question about the Discover AI corpus…"
          disabled={isRunning}
        />
        <div className="mt-3 flex items-center justify-between">
          <span className="text-xs text-muted-foreground">
            Discover AI transcript corpus
          </span>
          <button
            className="rounded-md bg-primary px-4 py-1.5 text-sm font-medium text-primary-foreground transition-opacity hover:opacity-90 disabled:opacity-40"
            onClick={() => runQuery(query)}
            disabled={isRunning || !query.trim()}
          >
            {isRunning ? "Running…" : "Ask"}
          </button>
        </div>
      </div>

      {/* Example prompts */}
      <div className="mt-3 flex flex-wrap gap-2">
        {EXAMPLE_PROMPTS.map((p) => (
          <button
            key={p}
            className="rounded-full border border-border bg-card px-3 py-1.5 text-left text-xs text-muted-foreground transition-colors hover:bg-muted disabled:opacity-50"
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

      {error && (
        <div className="mt-6 rounded-lg border border-destructive/30 bg-destructive/10 px-4 py-3 text-sm text-destructive">
          {error}
        </div>
      )}

      {/* Once a run starts: answer + sources in the main column, agent trace in the rail. */}
      {started && (
        <div className="mt-6 grid gap-6 lg:grid-cols-[1fr_320px]">
          <div className="min-w-0 space-y-6">
            <section>
              <div className="mb-3 text-sm font-semibold text-foreground">Answer</div>
              <div className="rounded-2xl border border-border bg-card p-5 shadow-sm">
                {answerText ? (
                  <div className="markdown-answer">
                    <ReactMarkdown>
                      {withCitationChips(answerText, citations)}
                    </ReactMarkdown>
                  </div>
                ) : (
                  <p className="animate-pulse text-sm text-muted-foreground">
                    Researching the corpus…
                  </p>
                )}
              </div>
              {evidence && (
                <VerificationStrip evidence={evidence} maxSteps={maxSteps} />
              )}
            </section>

            {citations.length > 0 && (
              <section>
                <div className="mb-3 text-sm font-semibold text-foreground">Sources</div>
                <Sources citations={citations} titles={titles} />
              </section>
            )}
          </div>

          <div className="lg:sticky lg:top-20 lg:self-start">
            <TracePanel
              trace={trace}
              thinking={thinking}
              tokens={tokens}
              elapsedMs={elapsedMs}
              isRunning={isRunning}
              citations={citations}
              titles={titles}
              evidence={evidence}
              runId={runId}
            />
          </div>
        </div>
      )}
    </main>
  );
}
