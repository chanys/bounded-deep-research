"use client";

// Cited evidence, grouped by video. One compact card per video: title +
// "N cited passages", then a scannable row per passage: [n] · time range · short
// evidence label (the citation reason). No thumbnails, no long excerpts. Each row
// carries id="source-n" so the inline [n] chips in the answer jump to it.
// Clicking a passage opens the in-page player modal at that timestamp (instead
// of navigating to YouTube, which tends not to give the user back).

import { useState } from "react";
import type { Citation } from "@/lib/events";
import { VideoModal } from "@/components/VideoModal";

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
  // The passage playing in the modal, or null when closed.
  const [playing, setPlaying] = useState<Citation | null>(null);

  // Group by video, preserving each citation's 1-based index (matches the chips).
  const groups = new Map<string, Passage[]>();
  citations.forEach((c, i) => {
    const list = groups.get(c.video_id) ?? [];
    list.push({ citation: c, index: i + 1 });
    groups.set(c.video_id, list);
  });

  return (
    <div className="space-y-3">
      {[...groups.entries()].map(([videoId, passages]) => (
        <div key={videoId} className="rounded-xl border border-border bg-card">
          <div className="flex gap-3 border-b border-border px-4 py-3">
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img
              src={`https://img.youtube.com/vi/${videoId}/hqdefault.jpg`}
              alt=""
              className="aspect-video w-24 shrink-0 rounded-md object-cover"
            />
            <div className="min-w-0">
              <div className="line-clamp-2 text-sm font-medium">
                {titles[videoId] ?? videoId}
              </div>
              <div className="mt-0.5 text-xs text-muted-foreground">
                {passages.length} cited passage{passages.length > 1 ? "s" : ""}
              </div>
            </div>
          </div>
          <ul className="divide-y divide-border">
            {passages.map(({ citation: c, index }) => (
              <li key={index} id={`source-${index}`} className="scroll-mt-20">
                <button
                  onClick={() => setPlaying(c)}
                  className="flex w-full items-baseline gap-2.5 px-4 py-2 text-left transition-colors hover:bg-muted/50"
                >
                  <span className="shrink-0 font-mono text-xs font-semibold text-indigo-600">
                    [{index}]
                  </span>
                  <span className="shrink-0 font-mono text-xs text-muted-foreground">
                    {timestamp(c.start_ts)}–{timestamp(c.end_ts)}
                  </span>
                  {c.reason && (
                    <span className="min-w-0 text-sm text-foreground">{c.reason}</span>
                  )}
                </button>
              </li>
            ))}
          </ul>
        </div>
      ))}

      {playing && (
        <VideoModal
          videoId={playing.video_id}
          startTs={playing.start_ts}
          title={titles[playing.video_id] ?? playing.video_id}
          onClose={() => setPlaying(null)}
        />
      )}
    </div>
  );
}
