// Renders one RunEvidence record: the harness state for a single run. This is the
// "the harness is inspectable in the live system" panel. It only displays what the
// backend already computed; it does no analysis of its own.

import type { RunEvidence } from "@/lib/api";

function Stat({ label, value, warn }: { label: string; value: React.ReactNode; warn?: boolean }) {
  return (
    <div className="rounded-lg border border-border bg-card p-3">
      <div className="text-xs text-muted-foreground">{label}</div>
      <div className={`text-lg font-mono ${warn ? "text-red-600" : "text-foreground"}`}>{value}</div>
    </div>
  );
}

function ChunkList({ label, ids, warnIfAny }: { label: string; ids: string[]; warnIfAny?: boolean }) {
  const bad = warnIfAny && ids.length > 0;
  return (
    <div className="rounded-lg border border-border bg-card p-3">
      <div className={`text-xs ${bad ? "text-red-600" : "text-muted-foreground"}`}>
        {label} ({ids.length})
      </div>
      {ids.length === 0 ? (
        <div className="text-sm text-muted-foreground">none</div>
      ) : (
        <ul className="mt-1 space-y-0.5 font-mono text-xs text-foreground">
          {ids.map((id) => (
            <li key={id}>{id}</li>
          ))}
        </ul>
      )}
    </div>
  );
}

export function RunAudit({ evidence: e }: { evidence: RunEvidence }) {
  return (
    <div className="space-y-4">
      {/* Run identity */}
      <div className="text-sm">
        <div className="text-foreground">{e.query}</div>
        <div className="mt-1 font-mono text-xs text-muted-foreground">
          run {e.run_id}
          {e.trace_url && (
            <>
              {" · "}
              <a href={e.trace_url} target="_blank" rel="noopener noreferrer" className="underline">
                Langfuse trace
              </a>
            </>
          )}
        </div>
      </div>

      {/* Config + outcome */}
      <div className="grid grid-cols-2 gap-2 sm:grid-cols-4">
        <Stat label="recipe" value={e.recipe_version} />
        <Stat label="mode" value={e.retrieval_mode} />
        <Stat label="model" value={e.model} />
        <Stat label="steps" value={e.steps_used} />
        <Stat label="budget exhausted" value={e.budget_exhausted ? "yes" : "no"} warn={e.budget_exhausted} />
        <Stat label="citations valid" value={e.citations_valid ? "yes" : "no"} warn={!e.citations_valid} />
        <Stat label="cost (USD)" value={`$${e.usd_cost.toFixed(4)}`} />
        <Stat label="total tokens" value={e.usage.total_tokens.toLocaleString()} />
      </div>

      {/* Retrieval activity */}
      <div className="grid grid-cols-2 gap-2 sm:grid-cols-3">
        <Stat label="searches" value={e.search_count} />
        <Stat label="chunks seen" value={e.seen_count} />
        <Stat label="chunks cited" value={e.cited_count} />
      </div>

      {/* Behavioral metrics */}
      <div className="grid grid-cols-2 gap-2">
        <Stat
          label="duplicate search rate"
          value={`${Math.round(e.duplicate_search_rate * 100)}%`}
          warn={e.duplicate_search_rate >= 0.5}
        />
      </div>

      <div className="grid grid-cols-1 gap-2">
        <ChunkList label="cited but not retrieved" ids={e.cited_not_retrieved} warnIfAny />
      </div>
    </div>
  );
}
