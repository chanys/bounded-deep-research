"use client";

// In-page video player: a modal with the YouTube IFrame embed cued to the cited
// timestamp, so following a citation doesn't navigate away from the answer.
// youtube-nocookie.com is the privacy-enhanced embed host (no tracking cookies
// until playback starts). Some videos disable embedding; the header keeps a
// plain YouTube link as the escape hatch.

import { useEffect } from "react";
import { ExternalLink, X } from "lucide-react";

export function VideoModal({
  videoId,
  startTs,
  title,
  onClose,
}: {
  videoId: string;
  startTs: number;
  title: string;
  onClose: () => void;
}) {
  // Close on Escape; backdrop click closes via the outer onClick below.
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    document.addEventListener("keydown", onKey);
    return () => document.removeEventListener("keydown", onKey);
  }, [onClose]);

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-label={title}
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4"
      onClick={onClose}
    >
      <div
        className="w-full max-w-3xl overflow-hidden rounded-2xl border border-border bg-card shadow-lg"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-center gap-3 border-b border-border px-4 py-3">
          <div className="min-w-0 flex-1 truncate text-sm font-medium">{title}</div>
          <a
            href={`https://www.youtube.com/watch?v=${videoId}&t=${startTs}s`}
            target="_blank"
            rel="noopener noreferrer"
            className="flex shrink-0 items-center gap-1 text-xs text-muted-foreground transition-colors hover:text-foreground"
          >
            <ExternalLink className="h-3.5 w-3.5" />
            YouTube
          </a>
          <button
            aria-label="Close"
            onClick={onClose}
            className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full text-muted-foreground transition-colors hover:bg-muted hover:text-foreground"
          >
            <X className="h-4 w-4" />
          </button>
        </div>
        <div className="aspect-video bg-black">
          <iframe
            className="h-full w-full"
            src={`https://www.youtube-nocookie.com/embed/${videoId}?start=${startTs}&autoplay=1`}
            title={title}
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowFullScreen
          />
        </div>
      </div>
    </div>
  );
}
