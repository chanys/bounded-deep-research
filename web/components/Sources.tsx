// Cited evidence, grouped by video so distinct sources stand out instead of
// repeating the same thumbnail. One block per video (thumbnail + title once),
// then each cited passage as a row: [n] · time range · why it was used. Each row
// carries id="source-n" so the inline [n] chips in the answer jump to it.

import type { Citation } from "@/lib/events";

function timestamp(seconds: number): string {
  const m = Math.floor(seconds / 60);
  const s = seconds % 60;
  return `${m}:${String(s).padStart(2, "0")}`;
}

type Passage = { citation: Citation; index: number };

export function Sources({
  citations,
  titles,
}: {
  citations: Citation[];
  titles: Record<string, string>;
}) {
  // Group by video while preserving each citation's 1-based index (which matches
  // the inline chips). Insertion order of the Map keeps videos in first-cited order.
  const groups = new Map<string, Passage[]>();
  citations.forEach((c, i) => {
    const list = groups.get(c.video_id) ?? [];
    list.push({ citation: c, index: i + 1 });
    groups.set(c.video_id, list);
  });

  return (
    <div className="space-y-3">
      {[...groups.entries()].map(([videoId, passages]) => (
        <div
          key={videoId}
          className="overflow-hidden rounded-xl border border-border bg-card"
        >
          <div className="flex gap-3 p-3">
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img
              src={`https://img.youtube.com/vi/${videoId}/hqdefault.jpg`}
              alt=""
              className="aspect-video w-28 shrink-0 rounded-md object-cover"
            />
            <div className="min-w-0">
              <div className="line-clamp-2 text-sm font-medium leading-snug">
                {titles[videoId] ?? videoId}
              </div>
              <div className="mt-1 text-xs text-muted-foreground">
                {passages.length} cited passage{passages.length > 1 ? "s" : ""}
              </div>
            </div>
          </div>

          <ul className="divide-y divide-border border-t border-border">
            {passages.map(({ citation: c, index }) => (
              <li key={index} id={`source-${index}`} className="scroll-mt-20">
                <a
                  href={`https://www.youtube.com/watch?v=${c.video_id}&t=${c.start_ts}s`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex gap-2.5 px-3 py-2.5 transition-colors hover:bg-muted/50"
                >
                  <span className="mt-0.5 shrink-0 rounded bg-indigo-50 px-1.5 text-xs font-semibold text-indigo-600">
                    {index}
                  </span>
                  <div className="min-w-0">
                    <div className="font-mono text-xs text-muted-foreground">
                      {timestamp(c.start_ts)}–{timestamp(c.end_ts)}
                    </div>
                    {c.reason && (
                      <div className="mt-0.5 text-sm text-foreground">{c.reason}</div>
                    )}
                  </div>
                </a>
              </li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
}
