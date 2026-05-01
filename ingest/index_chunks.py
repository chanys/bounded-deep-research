"""Create OpenSearch index and bulk-load all embedded chunks for a channel.

Drops and recreates the index per run. Reads chunks + embeddings from
Postgres (source of truth). Postgres marks all included videos as
indexed after refresh.

Usage:
  uv run python -m ingest.index_chunks --channel code4AI
"""
import argparse

from opensearchpy import OpenSearch, helpers
from tqdm import tqdm

from app.config import settings
from app.db import transaction

# This mapping gives us:
# - BM25 over `text` and `title`
# - kNN over `embedding`
# - exact fetch by `chunk_id`
# - filter by `channel`, `published_at`
# - hybrid queries that combine BM25 + kNN + filters in one request
MAPPING = {
    "settings": {
        "index": {
            "knn": True,  # turns on kNN search at the index level
            "number_of_shards": 1,  # split the index into one piece
            "number_of_replicas": 0,
        }
    },
    "mappings": {
        "properties": {
            "chunk_id":     {"type": "keyword"},  # exactly match, used for filtering
            "video_id":     {"type": "keyword"},  # exactly match, used for filtering
            "title":        {"type": "text", "analyzer": "standard"},  # full-text-searchable. The standard analyzer lowercases + splits on whitespace/punctuation into tokens.
            "channel":      {"type": "keyword"},  # exactly match, used for filtering
            "published_at": {"type": "date"},     # supports range query
            "start_ts":     {"type": "integer"},  # numeric, range-queryable, exact-match-filterable
            "end_ts":       {"type": "integer"},  # numeric, range-queryable, exact-match-filterable
            "text":         {"type": "text", "analyzer": "standard"},  # full-text-searchable
            "embedding": {
                "type": "knn_vector",
                "dimension": 3072,
                "method": {
                    "name": "hnsw",  # the standard ANN algo for vector search
                    "engine": "lucene",  # three engines exist (Lucene, nmslib, FAISS); Lucene is OpenSearch-native, lowest operational complexity
                    "space_type": "cosinesimil",
                },
            },
        }
    },
}


def fetch_docs(channel: str, index: str):
    """Yield bulk actions for streaming_bulk. Reads from video_chunks JOIN videos."""
    with transaction() as conn:
        rows = conn.execute("""
            SELECT
              c.chunk_id,
              c.video_id,
              c.start_s AS start_ts,
              c.end_s AS end_ts,
              c.text,
              c.embedding,
              v.title,
              v.channel,
              v.published_at
            FROM video_chunks c
            JOIN videos v USING (video_id)
            WHERE v.channel = %s
              AND c.embedded_at IS NOT NULL
            ORDER BY c.video_id, c.start_s
        """, (channel,)).fetchall()

    for r in rows:
        yield {
            "_op_type": "index",
            "_index": index,
            "_id": r["chunk_id"],
            "chunk_id": r["chunk_id"],
            "video_id": r["video_id"],
            "title": r["title"],
            "channel": r["channel"],
            "published_at": r["published_at"].isoformat() if r["published_at"] else None,
            "start_ts": r["start_ts"],
            "end_ts": r["end_ts"],
            "text": r["text"],
            "embedding": list(r["embedding"]),
        }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--channel", required=True, help="channel slug, e.g. code4AI")
    p.add_argument("--host", default="localhost")
    p.add_argument("--port", type=int, default=9200)
    args = p.parse_args()

    index = f"{settings.opensearch_index_prefix}_{args.channel}".lower()

    # Source-of-truth count for verification.
    with transaction() as conn:
        total = conn.execute("""
            SELECT COUNT(*) AS n FROM video_chunks c
            JOIN videos v USING (video_id)
            WHERE v.channel = %s AND c.embedded_at IS NOT NULL
        """, (args.channel,)).fetchone()["n"]

    if total == 0:
        print("no embedded chunks to index")
        return

    print(f"indexing {total} chunks into '{index}'")

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

    success = 0
    for ok, _ in tqdm(
        helpers.streaming_bulk(client, fetch_docs(args.channel, index),
                               chunk_size=500, raise_on_error=True),
        total=total, desc="indexing",
    ):
        if ok:
            success += 1

    client.indices.refresh(index=index)

    if success != total:
        raise RuntimeError(f"indexed {success} != source count {total}")

    os_count = client.count(index=index)["count"]
    if os_count != total:
        raise RuntimeError(f"OpenSearch reports {os_count}, expected {total}")

    print(f"indexed {success} chunks; OpenSearch count verified")

    # Mark all included videos as indexed.
    with transaction() as conn:
        conn.execute("""
            UPDATE videos SET indexed_at = NOW()
            WHERE channel = %s
              AND chunked_at IS NOT NULL
              AND video_id IN (
                SELECT DISTINCT video_id FROM video_chunks WHERE embedded_at IS NOT NULL
              )
        """, (args.channel,))


if __name__ == "__main__":
    main()