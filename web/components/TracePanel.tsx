// The agent's run shown as a human-readable research audit, not raw logs. It
// answers "what did the agent do, and why trust the result?" via numbered steps
// (search / read / synthesize / validate) plus a budget summary. Raw identifiers
// (run id, chunk ids) live under a "Debug details" expansion. Lives in the right
// rail; presentational only (event handling and id correlation stay in the page).

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

function ts(seconds: number): string {
  const m = Math.floor(seconds / 60);
  const s = seconds % 60;
  return `${m}:${String(s).padStart(2, "0")}`;
}

function Step({ n, title, children }: { n: number; title: string; children?: React.ReactNode }) {
  return (
    <li className="flex gap-3">
      <span className="mt-0.5 flex h-5 w-5 shrink-0 items-center justify-center rounded-full border border-border bg-muted text-[10px] font-semibold text-muted-foreground">
        {n}
      </span>
      <div className="min-w-0">
        <div className="text-sm font-medium text-foreground">{title}</div>
        {children}
      </div>
    </li>
  );
}

export function TracePanel({
  trace,
  thinking,
  tokens,
  elapsedMs,
  isRunning,
  citations,
  titles,
  evidence,
  runId,
}: {
  trace: TraceItem[];
  thinking: boolean;
  tokens: number;
  elapsedMs: number;
  isRunning: boolean;
  citations: Citation[];
  titles: Record<string, string>;
  evidence: RunEvidence | null;
  runId: string | null;
}) {
  const searchCount = trace.filter((t) => t.kind === "search").length;
  const readCount = trace.filter((t) => t.kind === "read" && t.status === "ok").length;
  const distinctSources = new Set(citations.map((c) => c.video_id)).size;

  // Number the steps as we go: each trace item, then synthesize + validate at the end.
  let n = 0;

  return (
    <aside className="rounded-xl border border-border bg-card">
      <div className="border-b border-border px-4 py-3">
        <div className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
          Research Trace
        </div>
        <div className="mt-1.5 text-xs text-muted-foreground">
          {Math.floor(elapsedMs / 1000)}s · {tokens.toLocaleString()} tokens
          {evidence ? ` · $${evidence.usd_cost.toFixed(4)}` : ""}
        </div>
        <div className="text-xs text-muted-foreground">
          {evidence ? `${evidence.steps_used} steps · ` : ""}
          {searchCount} searches · {readCount} chunks read
          {thinking && <span className="ml-2 animate-pulse text-amber-600">● thinking</span>}
        </div>
      </div>

      <ol className="space-y-3 px-4 py-4">
        {trace.length === 0 && (
          <li className="text-xs text-muted-foreground/60">
            {isRunning ? "starting…" : "no activity yet"}
          </li>
        )}

        {trace.map((item) =>
          item.kind === "search" ? (
            <Step key={`s-${item.id}`} n={++n} title="Searched transcript corpus">
              <div className="truncate text-sm text-muted-foreground">“{item.query}”</div>
              <div className="text-xs text-muted-foreground/70">
                {item.resultCount === null
                  ? "searching…"
                  : `${item.resultCount} candidate passages`}
              </div>
            </Step>
          ) : (
            <Step
              key={`r-${item.id}`}
              n={++n}
              title={item.status === "not_found" ? "Read failed" : "Read passage"}
            >
              {titles[item.videoId] && (
                <div className="line-clamp-1 text-sm text-muted-foreground">
                  {titles[item.videoId]}
                </div>
              )}
              <div className="text-xs text-muted-foreground/70">
                {item.endTs ? `${ts(item.startTs)}–${ts(item.endTs)}` : ts(item.startTs)}
                {item.status === "reading" && " · reading…"}
                {item.status === "not_found" && " · not found"}
              </div>
            </Step>
          ),
        )}

        {/* Synthesize + validate, derived once the run finishes. */}
        {citations.length > 0 && (
          <Step n={++n} title="Generated answer">
            <div className="text-xs text-muted-foreground/70">
              {citations.length} cited passage{citations.length > 1 ? "s" : ""} from{" "}
              {distinctSources} source{distinctSources > 1 ? "s" : ""}
            </div>
          </Step>
        )}
        {evidence && (
          <Step n={++n} title="Validated citations">
            <div
              className={`text-xs ${
                evidence.citations_valid && evidence.read_before_cite_violations.length === 0
                  ? "text-muted-foreground/70"
                  : "text-red-600"
              }`}
            >
              {!evidence.citations_valid
                ? "validation failed"
                : evidence.read_before_cite_violations.length > 0
                  ? `${evidence.read_before_cite_violations.length} cited without reading`
                  : "all cited passages matched"}
            </div>
          </Step>
        )}
      </ol>

      {/* Raw identifiers, for reproducing or inspecting the exact run. */}
      {(runId || trace.some((t) => t.kind === "read")) && (
        <details className="border-t border-border px-4 py-2">
          <summary className="cursor-pointer text-xs text-muted-foreground">
            Debug details
          </summary>
          <div className="mt-2 space-y-1 break-all font-mono text-[11px] text-muted-foreground/80">
            {runId && <div>run_id: {runId}</div>}
            {trace
              .filter((t): t is Extract<TraceItem, { kind: "read" }> => t.kind === "read")
              .map((t) => (
                <div key={`d-${t.id}`}>
                  {t.videoId}:{String(t.startTs).padStart(5, "0")}
                </div>
              ))}
          </div>
        </details>
      )}
    </aside>
  );
}
