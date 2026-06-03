"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { ArchitectureDiagram } from "@/components/ArchitectureDiagram";
import { RunAudit } from "@/components/RunAudit";
import { fetchLatestEvidence, fetchRunEvidence, type RunEvidence } from "@/lib/api";

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <section className="mb-10">
      <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-zinc-500">
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
    <main className="max-w-3xl mx-auto p-8 font-sans">
      <div className="mb-8 flex items-baseline justify-between">
        <h1 className="text-2xl font-semibold">System</h1>
        <Link href="/query" className="text-sm text-zinc-500 underline">
          ← back to query
        </Link>
      </div>

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
              className="rounded border border-zinc-200 px-3 py-1.5 hover:bg-zinc-50"
            >
              Latest run in Langfuse →
            </a>
          )}
          <a
            href="https://platform.openai.com/usage"
            target="_blank"
            rel="noopener noreferrer"
            className="rounded border border-zinc-200 px-3 py-1.5 hover:bg-zinc-50"
          >
            OpenAI usage dashboard →
          </a>
        </div>
      </Section>

      <Section title="Eval results">
        <div className="rounded border border-dashed border-zinc-300 p-4 text-sm text-zinc-500">
          Calibrated-judge eval results land in Phase 4.
        </div>
      </Section>

      <Section title="Run audit">
        <div className="mb-3 flex flex-wrap items-center gap-2">
          <button
            onClick={loadLatest}
            className="rounded border border-zinc-200 px-3 py-1.5 text-sm hover:bg-zinc-50"
          >
            Load latest
          </button>
          <input
            value={lookupId}
            onChange={(ev) => setLookupId(ev.target.value)}
            onKeyDown={(ev) => ev.key === "Enter" && loadById()}
            placeholder="run id…"
            className="flex-1 rounded border border-zinc-300 px-3 py-1.5 font-mono text-xs"
          />
          <button
            onClick={loadById}
            disabled={!lookupId.trim()}
            className="rounded border border-zinc-200 px-3 py-1.5 text-sm hover:bg-zinc-50 disabled:opacity-50"
          >
            Load
          </button>
        </div>

        {loading ? (
          <p className="text-sm text-zinc-400">Loading…</p>
        ) : evidence ? (
          <RunAudit evidence={evidence} />
        ) : (
          <p className="text-sm text-zinc-400">
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
