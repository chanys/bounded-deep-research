"""Create OpenSearch index and bulk-load all chunked videos for a channel.

Drops and recreates the index per run. Postgres marks all included videos
as indexed after refresh.

Usage:
  uv run python -m ingest.index_chunks --channel code4AI
"""
import argparse
import json
from pathlib import Path

from opensearchpy import OpenSearch, helpers

from app.config import settings
from app.db import transaction

MAPPING = {
    "mappings": {
        "properties": {
            "video_id": {"type": "keyword"},
            "title":    {"type": "text", "analyzer": "standard"},
            "start_ts": {"type": "integer"},
            "end_ts":   {"type": "integer"},
            "text":     {"type": "text", "analyzer": "standard"},
        }
    }
}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--channel", required=True, help="channel slug, e.g. code4AI")
    p.add_argument("--host", default="localhost")
    p.add_argument("--port", type=int, default=9200)
    args = p.parse_args()

    CHUNKS_DIR = Path(f"data/chunks/{args.channel}")
    index = f"{settings.opensearch_index_prefix}_{args.channel}".lower()

    # Get the set of chunked videos from Postgres — the source of truth
    # for what should be in the index.
    with transaction() as conn:
        rows = conn.execute("""
            SELECT video_id FROM videos
            WHERE channel = %s AND chunked_at IS NOT NULL
            ORDER BY published_at
        """, (args.channel,)).fetchall()

    if not rows:
        print("no chunked videos to index")
        return

    video_ids = [r["video_id"] for r in rows]
    print(f"indexing {len(video_ids)} videos into '{index}'")

    client = OpenSearch(
        hosts=[{"host": args.host, "port": args.port}],
        use_ssl=False,
        verify_certs=False,
    )

    if client.indices.exists(index=index):
        print(f"dropping existing index '{index}'")
        client.indices.delete(index=index)

    client.indices.create(index=index, body=MAPPING)
    print(f"created index '{index}'")

    def gen():
        for video_id in video_ids:
            path = CHUNKS_DIR / f"{video_id}.jsonl"
            for line in path.read_text().splitlines():
                chunk = json.loads(line)
                yield {"_index": index, "_source": chunk}

    n, _ = helpers.bulk(client, gen())
    client.indices.refresh(index=index)
    print(f"indexed {n} chunks")

    # Mark all included videos as indexed.
    with transaction() as conn:
        conn.execute("""
            UPDATE videos SET indexed_at = NOW()
            WHERE channel = %s AND chunked_at IS NOT NULL
        """, (args.channel,))
    print(f"marked {len(video_ids)} videos as indexed")


if __name__ == "__main__":
    main()