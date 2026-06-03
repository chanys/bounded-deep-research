// One cited chunk, rendered as a card that deep-links into the YouTube video at
// the citation's start time. Thumbnail and link are derived from the video id;
// the title comes from the batch hydrate call (falls back to the id).

import { Card, CardContent } from "@/components/ui/card";
import type { Citation } from "@/lib/events";

function timestamp(seconds: number): string {
  const m = Math.floor(seconds / 60);
  const s = seconds % 60;
  return `${m}:${String(s).padStart(2, "0")}`;
}

export function CitationCard({
  citation,
  title,
}: {
  citation: Citation;
  title?: string;
}) {
  const { video_id, start_ts, end_ts } = citation;
  const href = `https://www.youtube.com/watch?v=${video_id}&t=${start_ts}s`;
  const thumbnail = `https://img.youtube.com/vi/${video_id}/hqdefault.jpg`;

  return (
    <a href={href} target="_blank" rel="noopener noreferrer" className="block">
      <Card className="overflow-hidden hover:bg-zinc-50 transition-colors">
        <CardContent className="flex gap-3 p-0">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img src={thumbnail} alt="" className="w-32 shrink-0 object-cover" />
          <div className="py-2 pr-3">
            <div className="text-sm font-medium line-clamp-2">
              {title ?? video_id}
            </div>
            <div className="mt-1 font-mono text-xs text-zinc-500">
              {timestamp(start_ts)}–{timestamp(end_ts)}
            </div>
          </div>
        </CardContent>
      </Card>
    </a>
  );
}
