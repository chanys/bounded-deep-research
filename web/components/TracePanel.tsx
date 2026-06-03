// Right rail: the run shown as a polished audit panel. Two sections:
//  - Research steps: raw search/read/answer/validate events grouped into four
//    human-readable categories with Lucide icons (no step numbers, no raw ids).
//  - Run details: production/reliability metrics from the run evidence.
// Presentational only; event handling and id correlation stay in the page.

import { Search, BookOpen, Sparkles, ShieldCheck } from "lucide-react";
import type { Citation } from "@/lib/events";
import type { RunEvidence } from "@/lib/api";

export type TraceItem =
  | { kind: "search"; id: number; query: string; resultCount: number | null }
  | {
      kind: "read";
      id: number;
      videoId: string;
      startTs: number;
      endTs?: number;
      status: "reading" | "ok" | "not_found";
    };

function StepRow({
  icon: Icon,
  active,
  title,
  detail,
}: {
  icon: typeof Search;
  active: boolean;
  title: string;
  detail?: string;
}) {
  return (
    <li className="flex gap-3">
      <Icon
        className={`mt-0.5 h-4 w-4 shrink-0 ${active ? "animate-pulse text-amber-600" : "text-muted-foreground"}`}
      />
      <div className="min-w-0">
        <div className="text-sm font-medium text-foreground">{title}</div>
        {detail && <div className="text-xs text-muted-foreground">{detail}</div>}
      </div>
    </li>
  );
}

function Detail({ label, children, warn }: { label: string; children: React.ReactNode; warn?: boolean }) {
  return (
    <div className="flex items-baseline justify-between gap-3 py-1">
      <span className="text-xs text-muted-foreground">{label}</span>
      <span className={`text-right text-xs font-medium ${warn ? "text-red-600" : "text-foreground"}`}>
        {children}
      </span>
    </div>
  );
}

const plural = (n: number, word: string) => `${n} ${word}${n === 1 ? "" : "s"}`;

export function TracePanel({
  trace,
  isRunning,
  answering,
  citations,
  evidence,
}: {
  trace: TraceItem[];
  isRunning: boolean;
  answering: boolean;
  citations: Citation[];
  evidence: RunEvidence | null;
}) {
  const searchCount = trace.filter((t) => t.kind === "search").length;
  const reads = trace.filter((t): t is Extract<TraceItem, { kind: "read" }> => t.kind === "read");
  const readOk = reads.filter((r) => r.status === "ok");
  const distinctReadVideos = new Set(readOk.map((r) => r.videoId)).size;

  // Current phase, used to mark one step "active" (present tense + pulse) while running.
  const phase = answering ? "wrote" : reads.length > 0 ? "read" : "search";
  const activeIf = (p: string) => isRunning && phase === p;

  return (
    <div className="space-y-4">
      {/* Research steps */}
      <section className="rounded-xl border border-border bg-card">
        <div className="border-b border-border px-4 py-3 text-xs font-semibold uppercase tracking-wide text-muted-foreground">
          {isRunning ? "Researching…" : "Research steps"}
        </div>
        <ol className="space-y-3 px-4 py-4">
          {(isRunning || searchCount > 0) && (
            <StepRow
              icon={Search}
              active={activeIf("search")}
              title={activeIf("search") ? "Searching transcript corpus" : "Searched transcript corpus"}
              detail={plural(searchCount, "search").replace("searchs", "searches")}
            />
          )}
          {reads.length > 0 && (
            <StepRow
              icon={BookOpen}
              active={activeIf("read")}
              title={activeIf("read") ? "Reading relevant passages" : "Read relevant passages"}
              detail={`${plural(readOk.length, "passage")} from ${plural(distinctReadVideos, "video")}`}
            />
          )}
          {answering && (
            <StepRow
              icon={Sparkles}
              active={activeIf("wrote")}
              title={activeIf("wrote") ? "Writing answer" : "Wrote answer"}
              detail={citations.length > 0 ? `Used ${plural(citations.length, "cited passage")}` : undefined}
            />
          )}
          {evidence && (
            <StepRow
              icon={ShieldCheck}
              active={false}
              title="Checked citations"
              detail={
                evidence.citations_valid && evidence.read_before_cite_violations.length === 0
                  ? "All citations matched cited passages"
                  : !evidence.citations_valid
                    ? "Validation failed"
                    : `${plural(evidence.read_before_cite_violations.length, "citation")} without a read`
              }
            />
          )}
        </ol>
      </section>

      {/* Run details */}
      {evidence && (
        <section className="rounded-xl border border-border bg-card">
          <div className="border-b border-border px-4 py-3 text-xs font-semibold uppercase tracking-wide text-muted-foreground">
            Run details
          </div>
          <div className="px-4 py-3">
            {evidence.trace_url && (
              <Detail label="Langfuse trace">
                <a href={evidence.trace_url} target="_blank" rel="noopener noreferrer" className="text-indigo-600 underline">
                  Open trace
                </a>
              </Detail>
            )}
            <Detail label="Model">{evidence.model}</Detail>
            <Detail label="Retrieval mode">{evidence.retrieval_mode}</Detail>
            <Detail label="Searches">{evidence.search_count}</Detail>
            <Detail label="Chunks retrieved">{evidence.seen_count}</Detail>
            <Detail label="Chunks cited">{evidence.cited_count}</Detail>
            <Detail label="Duplicate search rate">
              {Math.round(evidence.duplicate_search_rate * 100)}%
            </Detail>
            <Detail label="Cited without reading" warn={evidence.read_before_cite_violations.length > 0}>
              {evidence.read_before_cite_violations.length}
            </Detail>
            <Detail label="Cited but never surfaced" warn={evidence.cited_not_seen.length > 0}>
              {evidence.cited_not_seen.length}
            </Detail>
            <Detail label="Citations valid" warn={!evidence.citations_valid}>
              {evidence.citations_valid ? "Yes" : "No"}
            </Detail>
          </div>
        </section>
      )}
    </div>
  );
}
