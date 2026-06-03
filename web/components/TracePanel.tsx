// Live trace of the agent's retrieval activity, correlated by id.
// Searches and reads share one chronological list (appended on *_start, updated
// on *_complete by id), with a status line for elapsed time, cumulative tokens,
// and a "thinking" pulse while a model turn is in flight.

export type TraceItem =
  | { kind: "search"; id: number; query: string; resultCount: number | null }
  | {
      kind: "read";
      id: number;
      videoId: string;
      startTs: number;
      status: "reading" | "ok" | "not_found";
    };

export function TracePanel({
  trace,
  thinking,
  tokens,
  elapsedMs,
  isRunning,
}: {
  trace: TraceItem[];
  thinking: boolean;
  tokens: number;
  elapsedMs: number;
  isRunning: boolean;
}) {
  if (trace.length === 0 && !isRunning) return null;

  return (
    <div className="mb-8">
      <div className="flex items-center justify-between mb-2">
        <h2 className="text-sm font-semibold text-zinc-600">Trace</h2>
        <div className="flex items-center gap-3 text-xs font-mono text-zinc-500">
          <span>{Math.floor(elapsedMs / 1000)}s</span>
          <span>{tokens.toLocaleString()} tok</span>
          {thinking && (
            <span className="text-amber-600 animate-pulse">● thinking</span>
          )}
        </div>
      </div>

      <ul className="space-y-1 text-sm font-mono">
        {trace.map((item) =>
          item.kind === "search" ? (
            <li key={`s-${item.id}`}>
              <span className="text-zinc-400">search</span> {item.query}
              {item.resultCount === null ? (
                <span className="text-zinc-400"> … searching</span>
              ) : (
                <span className="text-zinc-500"> · {item.resultCount} results</span>
              )}
            </li>
          ) : (
            <li key={`r-${item.id}`}>
              <span className="text-zinc-400">read</span> {item.videoId} @ {item.startTs}s
              {item.status === "reading" ? (
                <span className="text-zinc-400"> … reading</span>
              ) : item.status === "ok" ? (
                <span className="text-zinc-500"> · done</span>
              ) : (
                <span className="text-red-500"> · not found</span>
              )}
            </li>
          ),
        )}
      </ul>
    </div>
  );
}
