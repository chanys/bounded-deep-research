"""List all code4AI videos -> data/channel_manifests/code4AI.jsonl"""
import json
import re
from pathlib import Path

from googleapiclient.discovery import build

from app.config import settings

# HANDLE = "@code4AI"
# OUT = Path("data/channel_manifests/code4AI.jsonl")

HANDLE = "@DwarkeshPatel"
OUT = Path("data/channel_manifests/DwarkeshPatel.jsonl")

def parse_duration(iso: str) -> int:
    """PT1H2M3S -> seconds"""
    m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso)
    h, m_, s = (int(x) if x else 0 for x in m.groups())
    return h * 3600 + m_ * 60 + s


def main():
    yt = build("youtube", "v3", developerKey=settings.youtube_api_key)

    # YouTube automatically maintains one "uploads" playlist per channel — you never see it in the UI, but it exists,
    # and it's the canonical way to enumerate a channel's videos via the API.
    # uploads_id is just that playlist's identifier (a string like "UUxxxxx..."),
    # which you pass to playlistItems().list() in the next step to page through the videos.
    uploads_id = yt.channels().list(
        part="contentDetails", forHandle=HANDLE
    ).execute()["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    videos, page = [], None
    while True:
        r = yt.playlistItems().list(
            part="contentDetails,snippet",
            playlistId=uploads_id,
            maxResults=50,   # API hard cap per page. 50 is the max YouTube allows for this endpoint.
            pageToken=page,  # pagination cursor
        ).execute()
        for item in r["items"]:
            videos.append({
                "id": item["contentDetails"]["videoId"],
                "title": item["snippet"]["title"],
                "publishedAt": item["contentDetails"]["videoPublishedAt"],
            })
        page = r.get("nextPageToken")
        if not page:
            break

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
            v.update(details.get(v["id"], {}))

    # Each item in `videos` is now a dict containing keys: id, title, publishedAt, duration_seconds, description, tags

    videos = [v for v in videos if v.get("duration_seconds", 0) > 180]  # filter out shorts

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w") as f:
        for v in videos:
            f.write(json.dumps(v, ensure_ascii=False) + "\n")

    print(f"Wrote {OUT} ({len(videos)} videos)")


if __name__ == "__main__":
    main()