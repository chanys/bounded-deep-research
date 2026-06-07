"use client";

import { useEffect, useRef, useState } from "react";
import ReactMarkdown from "react-markdown";
import { ArrowRight, Check, ChevronDown } from "lucide-react";
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
    title: "Ask TransGlobal TV",
    placeholder: "Ask a question about retirement, insurance, tax, or estate planning…",
    language: "zh",
    example_prompts: [
      "年金和人壽保險在退休規劃中各自扮演什麼角色？",
      "退休後要怎麼規劃才能少繳稅？",
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

  // Channel dropdown: open/closed state plus a click-outside listener to close it.
  // Custom (not a native <select>) because options render a logo image.
  const [pickerOpen, setPickerOpen] = useState(false);
  const pickerRef = useRef<HTMLDivElement>(null);
  useEffect(() => {
    if (!pickerOpen) return;
    const onMouseDown = (e: MouseEvent) => {
      if (pickerRef.current && !pickerRef.current.contains(e.target as Node)) {
        setPickerOpen(false);
      }
    };
    document.addEventListener("mousedown", onMouseDown);
    return () => document.removeEventListener("mousedown", onMouseDown);
  }, [pickerOpen]);

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

  // w-full on <main> matters: body is a flex column, so without an explicit
  // width this flex item would shrink-wrap to its content and the pane width
  // would vary with the (channel-dependent) text.
  return (
    <main className="mx-auto w-full max-w-7xl px-6 py-10 lg:grid lg:grid-cols-[230px_minmax(0,1fr)] lg:items-start lg:gap-8">
      {/* Channel rail: pick on the left, results in the center pane. Selecting only
          affects the next run; it also swaps the title, placeholder, and example
          cards. On small screens the rail becomes a horizontal row above the box. */}
      <aside className="mb-6 lg:sticky lg:top-6 lg:mb-0">
        <div className="mb-3 text-sm font-semibold text-foreground">Channel</div>
        <div ref={pickerRef} className="relative">
          <button
            aria-haspopup="listbox"
            aria-expanded={pickerOpen}
            className="flex w-full items-center gap-3 rounded-xl border border-border bg-card p-2.5 text-left text-sm shadow-sm transition-colors hover:bg-muted disabled:opacity-50"
            onClick={() => setPickerOpen((o) => !o)}
            disabled={isRunning}
          >
            <img
              src={`/channels/${channel.id}.jpg`}
              alt=""
              className="h-9 w-9 shrink-0 rounded-full object-cover"
            />
            <span className="min-w-0 flex-1">{channel.display_name}</span>
            <ChevronDown
              className={`h-4 w-4 shrink-0 text-muted-foreground transition-transform ${pickerOpen ? "rotate-180" : ""}`}
            />
          </button>
          {pickerOpen && (
            <div
              role="listbox"
              aria-label="Channel to search"
              className="absolute z-10 mt-2 w-full overflow-hidden rounded-xl border border-border bg-card shadow-md"
            >
              {channels.map((c) => (
                <button
                  key={c.id}
                  role="option"
                  aria-selected={c.id === channelId}
                  className={`flex w-full items-center gap-3 p-2.5 text-left text-sm transition-colors hover:bg-muted ${
                    c.id === channelId ? "bg-muted" : ""
                  }`}
                  onClick={() => {
                    setChannelId(c.id);
                    setPickerOpen(false);
                  }}
                >
                  <img
                    src={`/channels/${c.id}.jpg`}
                    alt=""
                    className="h-9 w-9 shrink-0 rounded-full object-cover"
                  />
                  <span className="min-w-0 flex-1">{c.display_name}</span>
                  {c.id === channelId && <Check className="h-4 w-4 shrink-0" />}
                </button>
              ))}
            </div>
          )}
        </div>
      </aside>

      <div className="min-w-0">
      <header className="mb-8">
        <h1 className="text-3xl font-semibold tracking-tight">{channel.title}</h1>
        <p className="mt-1 text-sm text-muted-foreground">
          Ask questions. Jump to the right video moment.
        </p>
      </header>

      {/* Persistent two-column split under the header: everything the user reads
          or writes (ask box, examples, answer, sources) shares the left column's
          width; the audit rail owns the right column from the start, so nothing
          changes width or jumps when a run starts. */}
      <div className="grid gap-6 lg:grid-cols-[minmax(0,1fr)_320px]">
      <div className="min-w-0">
      {/* Ask box: auto-sizing textarea with a round submit button. */}
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
          placeholder={channel.placeholder}
          disabled={isRunning}
        />
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
              taRef.current?.focus(); // let the user edit or confirm; submit stays manual
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

      {/* Once a run starts: answer + sources appear below the ask box, same column, same width. */}
      {started && (
        <div className="mt-8 space-y-6">
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
      )}
      </div>

      {/* The audit rail. Before the first run it's a placeholder (desktop only:
          on small screens the rail stacks below the content, where an empty box
          would just be clutter); during/after a run, the real panel. */}
      <div className="lg:sticky lg:top-6 lg:self-start">
        {started ? (
          <TracePanel
            trace={trace}
            isRunning={isRunning}
            answering={!!answerText}
            citations={citations}
            evidence={evidence}
            elapsedMs={elapsedMs}
            tokens={tokens}
          />
        ) : (
          <div className="hidden rounded-2xl border border-dashed border-border p-5 text-sm text-muted-foreground lg:block">
            Research steps and run details will appear here when you ask a question.
          </div>
        )}
      </div>
      </div>
      </div>
    </main>
  );
}
