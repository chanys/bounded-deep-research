"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { ArchitectureDiagram } from "@/components/ArchitectureDiagram";
import { RunAudit } from "@/components/RunAudit";
import { fetchLatestEvidence, fetchRunEvidence, type RunEvidence } from "@/lib/api";

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <section className="mb-10">
      <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-muted-foreground">
        {title}
      </h2>
      {children}
    </section>
  );
}

export default function SystemPage() {
  const [evidence, setEvidence] = useState<RunEvidence | null>(null);
  const [loading, setLoading] = useState(true);
  const [lookupId, setLookupId] = useState("");

  // Load the most recent run's evidence on mount.
  useEffect(() => {
    fetchLatestEvidence().then((e) => {
      setEvidence(e);
      setLoading(false);
    });
  }, []);

  const loadLatest = async () => {
    setLoading(true);
    setEvidence(await fetchLatestEvidence());
    setLoading(false);
  };

  const loadById = async () => {
    if (!lookupId.trim()) return;
    setLoading(true);
    setEvidence(await fetchRunEvidence(lookupId.trim()));
    setLoading(false);
  };

  return (
    <main className="mx-auto max-w-3xl px-6 py-10">
      <h1 className="mb-8 text-xl font-semibold tracking-tight">System</h1>

      <Section title="Architecture">
        <ArchitectureDiagram />
      </Section>

      <Section title="Cost & observability">
        <div className="flex flex-wrap gap-2 text-sm">
          {evidence?.trace_url && (
            <a
              href={evidence.trace_url}
              target="_blank"
              rel="noopener noreferrer"
              className="rounded-md border border-border bg-card px-3 py-1.5 hover:bg-muted"
            >
              Latest run in Langfuse →
            </a>
          )}
          <a
            href="https://platform.openai.com/usage"
            target="_blank"
            rel="noopener noreferrer"
            className="rounded-md border border-border bg-card px-3 py-1.5 hover:bg-muted"
          >
            OpenAI usage dashboard →
          </a>
        </div>
      </Section>

      <Section title="Eval results">
        <div className="rounded-md border border-dashed border-border p-4 text-sm text-muted-foreground">
          Calibrated-judge eval results land in Phase 4.
        </div>
      </Section>

      <Section title="Run audit">
        <div className="mb-3 flex flex-wrap items-center gap-2">
          <button
            onClick={loadLatest}
            className="rounded-md border border-border bg-card px-3 py-1.5 text-sm hover:bg-muted"
          >
            Load latest
          </button>
          <input
            value={lookupId}
            onChange={(ev) => setLookupId(ev.target.value)}
            onKeyDown={(ev) => ev.key === "Enter" && loadById()}
            placeholder="run id…"
            className="flex-1 rounded-md border border-input bg-card px-3 py-1.5 font-mono text-xs"
          />
          <button
            onClick={loadById}
            disabled={!lookupId.trim()}
            className="rounded-md border border-border bg-card px-3 py-1.5 text-sm hover:bg-muted disabled:opacity-50"
          >
            Load
          </button>
        </div>

        {loading ? (
          <p className="text-sm text-muted-foreground">Loading…</p>
        ) : evidence ? (
          <RunAudit evidence={evidence} />
        ) : (
          <p className="text-sm text-muted-foreground">
            No run found. Run a query on the{" "}
            <Link href="/query" className="underline">
              query page
            </Link>{" "}
            first.
          </p>
        )}
      </Section>
    </main>
  );
}
