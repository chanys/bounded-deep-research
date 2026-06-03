// Non-streaming REST calls to the backend. (The streaming /query call lives in
// sse.ts, which reuses API_BASE from here.)

export const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8000";

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
