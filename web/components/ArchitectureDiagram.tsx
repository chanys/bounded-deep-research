// Static architecture diagram for the /system page. Plain styled boxes (no
// diagramming dependency): a top-down flow from browser to agent, then a branch
// to the three backing services.

function Box({ title, subtitle }: { title: string; subtitle: string }) {
  return (
    <div className="rounded-lg border border-border bg-card px-4 py-3 text-center shadow-sm">
      <div className="text-sm font-semibold text-foreground">{title}</div>
      <div className="text-xs text-muted-foreground">{subtitle}</div>
    </div>
  );
}

function Arrow() {
  return <div className="text-muted-foreground/60">↓</div>;
}

export function ArchitectureDiagram() {
  return (
    <div className="flex flex-col items-center gap-2">
      <Box title="Browser (Next.js)" subtitle="query UI · live trace · run audit" />
      <Arrow />
      <Box title="FastAPI / uvicorn" subtitle="POST /query (SSE stream) · /runs/{id}/evidence" />
      <Arrow />
      <Box title="ReAct agent loop" subtitle="search · read · submit_answer, per-turn events" />
      <Arrow />
      <div className="grid w-full grid-cols-1 gap-2 sm:grid-cols-3">
        <Box title="OpenSearch" subtitle="BM25 + kNN over chunks" />
        <Box title="OpenAI" subtitle="agent model + embeddings" />
        <Box title="Postgres" subtitle="chunks + video titles" />
      </div>
    </div>
  );
}
