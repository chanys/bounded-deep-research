"use client";

import { useEffect, useRef, useState } from "react";
import ReactMarkdown from "react-markdown";
import { ArrowRight, ChevronDown } from "lucide-react";
import { TracePanel, type TraceItem } from "@/components/TracePanel";
import { Sources } from "@/components/Sources";
import type { Citation, SseEvent } from "@/lib/events";
import { streamQuery } from "@/lib/sse";
import { captureAccessCode } from "@/lib/access-code";
import {
  hydrateCitations,
  fetchLatestEvidence,
  fetchChannels,
  type Channel,
  type RunEvidence,
} from "@/lib/api";

// The model marks citations inline, but the exact form varies: either
// (video_id, start, end) tuples or [start-end] timestamp ranges (any dash). We
// rewrite each marker that maps to a known citation into a markdown link
// [n](#source-n), which renders as a numbered chip linking to its Sources row.
// A bracket range that doesn't match a real citation (e.g. a year range like
// [2025-2026]) is left untouched, as are all markers during streaming.
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
    // [video_id start-end]  (id, space, range)
    .replace(/\[([A-Za-z0-9_-]+)\s+(\d+)\s*[-–—]\s*(\d+)\]/g, (whole, vid, start, end) => {
      const n = byVidStart.get(`${vid}:${start}`) ?? byRange.get(`${start}-${end}`);
      return n ? `[${n}](#source-${n})` : whole;
    })
    // [start-end]  (range only, no id)
    .replace(/\[(\d+)\s*[-–—]\s*(\d+)\]/g, (whole, start, end) => {
      const n = byRange.get(`${start}-${end}`);
      return n ? `[${n}](#source-${n})` : whole;
    });
}

// Shown until GET /channels responds (and kept if it never does), so the page
// works even when the registry fetch fails. Mirrors the default (first) entry
// of app/channels.py; its id seeds the channel selection.
const FALLBACK_CHANNELS: Channel[] = [
  {
    id: "TransGlobalTV",
    display_name: "TransGlobal TV (泛宇財經頻道)",
    language: "zh",
    example_prompts: [
      "頻道如何比較年金與人壽保險在退休規劃中的角色？",
      "頻道對聯準會降息的看法在2025到2026年間有何變化？",
    ],
  },
];

export default function QueryPage() {
  const [query, setQuery] = useState("");
  const [channels, setChannels] = useState<Channel[]>(FALLBACK_CHANNELS);
  const [channelId, setChannelId] = useState(FALLBACK_CHANNELS[0].id);
  const [isRunning, setIsRunning] = useState(false);
  const [trace, setTrace] = useState<TraceItem[]>([]);
  const [tokens, setTokens] = useState(0); // accumulated across turns
  const [elapsedMs, setElapsedMs] = useState(0);
  const [answerText, setAnswerText] = useState(""); // grows from answer_delta, finalized by answer_complete
  const [citations, setCitations] = useState<Citation[]>([]);
  const [titles, setTitles] = useState<Record<string, string>>({}); // video_id -> title
  const [evidence, setEvidence] = useState<RunEvidence | null>(null); // fetched after the run
  const [error, setError] = useState<string | null>(null);

  // On load, capture an access code from ?k=CODE (e.g. a resume link) into sessionStorage
  // and scrub it from the URL. Subsequent queries send it for the higher quota.
  // Also load the channel registry; keep the selection if it survives the refresh.
  useEffect(() => {
    captureAccessCode();
    fetchChannels().then((list) => {
      if (list.length === 0) return; // fetch failed; stay on the fallback
      setChannels(list);
      setChannelId((id) => (list.some((c) => c.id === id) ? id : list[0].id));
    });
  }, []);

  // The selected channel drives the picker label and the example prompt cards.
  const channel = channels.find((c) => c.id === channelId) ?? channels[0];

  // Auto-size the input so it hugs the query text instead of a fixed tall box.
  const taRef = useRef<HTMLTextAreaElement>(null);
  useEffect(() => {
    const el = taRef.current;
    if (el) {
      el.style.height = "auto";
      el.style.height = `${el.scrollHeight}px`;
    }
  }, [query]);

  // Elapsed-time clock: ticks while a run is in flight, freezes when it ends.
  useEffect(() => {
    if (!isRunning) return;
    const start = performance.now();
    const id = setInterval(() => setElapsedMs(performance.now() - start), 1000);
    return () => clearInterval(id);
  }, [isRunning]);

  const handleEvent = (event: SseEvent) => {
    switch (event.type) {
      // Each completed model turn reports its token usage; accumulate it.
      case "turn_complete":
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
          { kind: "read", id: event.read_id, videoId: event.video_id, startTs: event.start_ts, status: "reading" },
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

      // Answer streams in piece by piece; answer_complete delivers the final text +
      // citations, then we fetch titles and the run evidence.
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
    setIsRunning(true);
    setTrace([]);
    setTokens(0);
    setElapsedMs(0);
    setAnswerText("");
    setCitations([]);
    setTitles({});
    setEvidence(null);
    setError(null);
    try {
      for await (const event of streamQuery({ query: q, channel: channelId })) {
        handleEvent(event);
      }
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      setIsRunning(false);
    }
  };

  const started = isRunning || !!answerText || trace.length > 0;

  return (
    <main className="mx-auto max-w-5xl px-6 py-10">
      <header className="mb-8">
        <h1 className="text-3xl font-semibold tracking-tight">AnswerTrail</h1>
        <p className="mt-1 text-sm text-muted-foreground">
          Deep research over YouTube channels
        </p>
      </header>

      {/* Ask box: auto-sizing textarea with a corpus pill and a round submit button. */}
      <div className="relative rounded-2xl border border-border bg-card shadow-sm">
        <textarea
          ref={taRef}
          rows={1}
          className="w-full resize-none overflow-hidden bg-transparent px-4 pb-14 pt-4 text-base outline-none placeholder:text-muted-foreground"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              runQuery(query);
            }
          }}
          placeholder="Ask a question about the corpus…"
          disabled={isRunning}
        />
        {/* Channel picker: the old corpus pill, now a select. Choosing a channel only
            affects the next run; it also swaps the example cards below. */}
        <div className="absolute bottom-3 left-3">
          <select
            aria-label="Channel to search"
            className="appearance-none rounded-full bg-muted py-1 pl-2.5 pr-7 text-xs text-muted-foreground outline-none hover:cursor-pointer disabled:opacity-50"
            value={channelId}
            onChange={(e) => setChannelId(e.target.value)}
            disabled={isRunning}
          >
            {channels.map((c) => (
              <option key={c.id} value={c.id}>
                {c.display_name}
              </option>
            ))}
          </select>
          <ChevronDown className="pointer-events-none absolute right-2 top-1/2 h-3 w-3 -translate-y-1/2 text-muted-foreground" />
        </div>
        <button
          aria-label="Ask"
          className="absolute bottom-3 right-3 flex h-9 w-9 items-center justify-center rounded-full bg-primary text-primary-foreground transition-opacity hover:opacity-90 disabled:opacity-40"
          onClick={() => runQuery(query)}
          disabled={isRunning || !query.trim()}
        >
          <ArrowRight className="h-4 w-4" />
        </button>
      </div>

      {/* Example cards for the selected channel, spanning the same width as the input. */}
      <div className="mt-3 grid grid-cols-1 gap-3 sm:grid-cols-2">
        {channel.example_prompts.map((p) => (
          <button
            key={p}
            className="rounded-xl border border-border bg-card p-3 text-left text-sm text-muted-foreground transition-colors hover:bg-muted disabled:opacity-50"
            onClick={() => {
              setQuery(p);
              runQuery(p);
            }}
            disabled={isRunning}
          >
            {p}
          </button>
        ))}
      </div>

      {error && (
        <div className="mt-6 rounded-lg border border-destructive/30 bg-destructive/10 px-4 py-3 text-sm text-destructive">
          {error}
        </div>
      )}

      {/* Once a run starts: answer + sources in the main column, the audit rail on the right. */}
      {started && (
        <div className="mt-8 grid gap-6 lg:grid-cols-[1fr_320px]">
          <div className="min-w-0 space-y-6">
            <section>
              <div className="mb-3 text-sm font-semibold text-foreground">Answer</div>
              <div className="rounded-2xl border border-border bg-card p-5 shadow-sm">
                {answerText ? (
                  <div className="markdown-answer">
                    <ReactMarkdown>{withCitationChips(answerText, citations)}</ReactMarkdown>
                  </div>
                ) : (
                  <p className="animate-pulse text-sm text-muted-foreground">Researching the corpus…</p>
                )}
              </div>
            </section>

            {citations.length > 0 && (
              <section>
                <div className="mb-3 text-sm font-semibold text-foreground">Sources</div>
                <Sources citations={citations} titles={titles} />
              </section>
            )}
          </div>

          <div className="lg:sticky lg:top-6 lg:self-start">
            <TracePanel
              trace={trace}
              isRunning={isRunning}
              answering={!!answerText}
              citations={citations}
              evidence={evidence}
              elapsedMs={elapsedMs}
              tokens={tokens}
            />
          </div>
        </div>
      )}
    </main>
  );
}
