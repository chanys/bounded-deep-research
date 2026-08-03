"""List a channel's or a playlist's videos -> data/channel_manifests/{name}.jsonl

A channel's uploads feed is itself just a playlist (YouTube auto-maintains one per
channel, id "UU..."), so both modes share the same enumeration code; --handle simply
resolves to that playlist id first.

Usage:
  uv run python -m ingest.list_channel_videos --handle @starterstory
  uv run python -m ingest.list_channel_videos --playlist PLxxxxxxxx --name SomeSeries
  uv run python -m ingest.list_channel_videos --playlist PLxxxxxxxx --name SomeSeries --min-duration 0

--name is the channel slug the rest of the pipeline keys on, i.e. what you later
pass as `--channel` to fetch_transcripts / register_channel. It defaults to the
handle without its "@", and is required for --playlist (a playlist id is not a name).
"""
import argparse
import json
import re
from collections import Counter
from pathlib import Path

from googleapiclient.discovery import build

from core.config import settings


# Full ISO 8601 duration as YouTube emits it. The day part sits before the T, so a
# PT-anchored pattern misses both "P0D" (what an upcoming live stream reports, having
# no content yet) and "P1DT2H" (anything over 24 hours).
_DURATION_RE = re.compile(r"^P(?:(\d+)D)?(?:T(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?)?$")


def parse_duration(iso: str) -> int:
    """ISO 8601 duration -> seconds. PT1H2M3S -> 3723; P0D -> 0; P1DT2H -> 93600."""
    m = _DURATION_RE.match(iso)
    if not m:
        raise ValueError(f"unparseable ISO 8601 duration from the API: {iso!r}")
    d, h, mi, s = (int(x) if x else 0 for x in m.groups())
    return d * 86400 + h * 3600 + mi * 60 + s


def resolve_uploads_playlist(yt, handle: str) -> str:
    """Handle (e.g. "@code4AI") -> that channel's uploads playlist id (e.g. "UU...").

    You never see this playlist in the UI, but it exists for every channel and is
    the canonical way to enumerate all of its videos via the API.
    """
    items = yt.channels().list(part="contentDetails", forHandle=handle).execute().get("items", [])
    if not items:
        raise SystemExit(f"no channel found for handle {handle}")
    return items[0]["contentDetails"]["relatedPlaylists"]["uploads"]


def list_playlist_items(yt, playlist_id: str) -> list[dict]:
    """Page through every item in a playlist.

    publishedAt comes from contentDetails.videoPublishedAt (when the video went
    live), NOT snippet.publishedAt (when it was added to the playlist) — those
    differ for curated playlists and only the former is meaningful for the corpus.
    """
    videos, page = [], None
    while True:
        r = yt.playlistItems().list(
            part="contentDetails,snippet",
            playlistId=playlist_id,
            maxResults=50,   # API hard cap per page. 50 is the max YouTube allows for this endpoint.
            pageToken=page,  # pagination cursor
        ).execute()
        for item in r["items"]:
            videos.append({
                "id": item["contentDetails"]["videoId"],
                "title": item["snippet"]["title"],
                "publishedAt": item["contentDetails"].get("videoPublishedAt"),
                "owner_channel": item["snippet"].get("videoOwnerChannelTitle"),
            })
        page = r.get("nextPageToken")
        if not page:
            break
    return videos


def attach_details(yt, videos: list[dict]) -> list[dict]:
    """Add duration/description/tags, dropping entries the videos endpoint won't return.

    Curated playlists routinely contain deleted or private videos. They still appear
    as playlist items but videos().list() omits them, so they would otherwise flow
    downstream with no duration and fail confusingly at fetch time. Drop them loudly
    here instead.
    """
    kept = []
    for i in range(0, len(videos), 50):
        batch = videos[i:i + 50]
        r = yt.videos().list(
            part="contentDetails,snippet",
            id=",".join(v["id"] for v in batch),
        ).execute()
        details = {
            item["id"]: {
                "duration_seconds": parse_duration(item["contentDetails"]["duration"]),
                "description": item["snippet"].get("description", ""),
                "tags": item["snippet"].get("tags", []),
            }
            for item in r["items"]
        }
        for v in batch:
            if v["id"] in details:
                kept.append({**v, **details[v["id"]]})

    dropped = len(videos) - len(kept)
    if dropped:
        print(f"  dropped {dropped} unavailable (deleted/private) videos")
    return kept


def main():
    p = argparse.ArgumentParser()
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("--handle", help='channel handle, e.g. "@starterstory"')
    src.add_argument("--playlist", help='playlist id from the URL\'s list= param, e.g. "PLxxxx"')
    p.add_argument("--name", help="channel slug for the manifest; defaults to handle without @")
    p.add_argument("--min-duration", type=int, default=180,
                   help="drop videos this long or shorter, in seconds (default 180, excludes Shorts; use 0 to keep all)")
    args = p.parse_args()

    name = args.name or (args.handle.lstrip("@") if args.handle else None)
    if not name:
        raise SystemExit("--name is required with --playlist")
    out = Path(f"data/channel_manifests/{name}.jsonl")

    yt = build("youtube", "v3", developerKey=settings.youtube_api_key)
    playlist_id = args.playlist or resolve_uploads_playlist(yt, args.handle)

    videos = list_playlist_items(yt, playlist_id)
    print(f"  {len(videos)} playlist items")
    videos = attach_details(yt, videos)

    # A playlist can mix creators, which would break the single-creator corpus
    # assumption the agent and the eval are built on. Surface it rather than hide it.
    owners = Counter(v["owner_channel"] for v in videos if v["owner_channel"])
    if len(owners) > 1:
        print(f"  WARNING: {len(owners)} distinct creators in this playlist: "
              + ", ".join(f"{o} ({n})" for o, n in owners.most_common()))

    # Each item in `videos` now has: id, title, publishedAt, owner_channel,
    # duration_seconds, description, tags
    if args.min_duration:
        before = len(videos)
        videos = [v for v in videos if v["duration_seconds"] > args.min_duration]
        print(f"  dropped {before - len(videos)} videos <= {args.min_duration}s")

    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w") as f:
        for v in videos:
            f.write(json.dumps(v, ensure_ascii=False) + "\n")

    print(f"Wrote {out} ({len(videos)} videos)")


if __name__ == "__main__":
    main()
