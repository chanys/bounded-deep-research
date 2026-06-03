// A row of real, computed signals shown under the answer: what makes this a
// bounded, verified run rather than a plain RAG answer. Every value comes from the
// run's RunEvidence (no fabricated confidence score). Problem signals turn red.

import type { RunEvidence } from "@/lib/api";

function Chip({ children, tone = "neutral" }: { children: React.ReactNode; tone?: "neutral" | "good" | "warn" }) {
  const toneCls =
    tone === "good"
      ? "border-emerald-200 bg-emerald-50 text-emerald-700"
      : tone === "warn"
        ? "border-red-200 bg-red-50 text-red-700"
        : "border-border bg-muted/40 text-muted-foreground";
  return (
    <span className={`rounded-full border px-2.5 py-1 text-xs font-medium ${toneCls}`}>
      {children}
    </span>
  );
}

export function VerificationStrip({
  evidence: e,
  maxSteps,
}: {
  evidence: RunEvidence;
  maxSteps: number | null;
}) {
  const unread = e.read_before_cite_violations.length;
  return (
    <div className="mt-3 flex flex-wrap gap-2">
      <Chip tone={e.citations_valid ? "good" : "warn"}>
        {e.citations_valid ? "✓ citations validated" : "✗ citation validation failed"}
      </Chip>
      <Chip>{e.cited_count} sources</Chip>
      <Chip>{e.read_count} chunks read</Chip>
      <Chip tone={e.budget_exhausted ? "warn" : "neutral"}>
        steps {e.steps_used}
        {maxSteps ? `/${maxSteps}` : ""}
      </Chip>
      <Chip>${e.usd_cost.toFixed(4)}</Chip>
      {unread > 0 && <Chip tone="warn">{unread} cited without reading</Chip>}
      {e.budget_exhausted && <Chip tone="warn">stopped at step budget</Chip>}
    </div>
  );
}
