// Non-streaming REST calls to the backend. (The streaming /query call lives in
// sse.ts, which reuses API_BASE from here.)

import type { TokenUsage } from "./events";

export const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8000";

// Mirror of app/channels.py Channel (minus its server-side prompt directive).
export type Channel = {
  id: string;
  display_name: string;
  title: string;
  placeholder: string;
  language: string;
  example_prompts: string[];
};

// Fetch the channel registry for the picker. Best-effort: on any failure returns
// [] and the caller keeps its built-in fallback, so the page works without it.
export async function fetchChannels(): Promise<Channel[]> {
  try {
    const res = await fetch(`${API_BASE}/channels`);
    if (!res.ok) return [];
    return (await res.json()) as Channel[];
  } catch {
    return [];
  }
}

// Mirror of app/evidence.py RunEvidenceState. Python sets serialize to JSON
// arrays, so seen/read/cited chunks come over as string[].
export type SearchEventRecord = {
  search_id: number;
  query: string;
  mode: string;
  returned_chunk_ids: string[];
  new_chunk_ids: string[];
  result_count: number;
};

export type ReadEventRecord = {
  read_id: number;
  chunk_id: string;
  video_id: string;
  start_ts: number;
  end_ts: number;
};

export type RunEvidence = {
  run_id: string;
  trace_url: string | null;
  query: string;
  channel: string;
  recipe_version: string;
  retrieval_mode: string;
  model: string;
  search_events: SearchEventRecord[];
  read_events: ReadEventRecord[];
  seen_chunks: string[];
  read_chunks: string[];
  cited_chunks: string[];
  search_count: number;
  read_count: number;
  seen_count: number;
  cited_count: number;
  duplicate_search_rate: number;
  consecutive_searches_without_read_max: number;
  read_before_cite_violations: string[];
  cited_not_seen: string[];
  usage: TokenUsage;
  per_turn_usage: TokenUsage[];
  usd_cost: number;
  cost_breakdown: Record<string, number>;
  steps_used: number;
  budget_exhausted: boolean;
  citations_valid: boolean;
};

// Fetch the harness evidence for the most recent run, or null if none / on error.
export async function fetchLatestEvidence(): Promise<RunEvidence | null> {
  try {
    const res = await fetch(`${API_BASE}/runs/latest/evidence`);
    if (!res.ok) return null;
    return (await res.json()) as RunEvidence;
  } catch {
    return null;
  }
}

// Fetch the harness evidence for a specific run id, or null if not found / on error.
export async function fetchRunEvidence(runId: string): Promise<RunEvidence | null> {
  try {
    const res = await fetch(`${API_BASE}/runs/${encodeURIComponent(runId)}/evidence`);
    if (!res.ok) return null;
    return (await res.json()) as RunEvidence;
  } catch {
    return null;
  }
}

// Resolve cited video ids to titles in one batch. Titles are best-effort: on any
// failure we return {} and the UI falls back to showing the video id.
export async function hydrateCitations(
  videoIds: string[],
): Promise<Record<string, string>> {
  if (videoIds.length === 0) return {};
  try {
    const res = await fetch(`${API_BASE}/citations/hydrate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ video_ids: videoIds }),
    });
    if (!res.ok) return {};
    return (await res.json()) as Record<string, string>;
  } catch {
    return {};
  }
}
