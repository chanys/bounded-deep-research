"""Create OpenSearch index and load all chunks from data/chunks/*.jsonl.

Drops and recreates the index each run (Day 2 one-shot; Phase 1 will add
proper idempotency).

Loads the per-video chunk JSONL files produced by chunk_transcripts.py into a local OpenSearch index named chunks.
On each run it drops and recreates the index with a fixed mapping (video_id as a keyword,
title and text as analyzed text fields using the standard analyzer, start_ts/end_ts as floats),
then streams all chunks from data/chunks/*.jsonl into OpenSearch via a bulk-load helper and
refreshes the index so documents are immediately searchable.
Idempotency is achieved by full recreation rather than per-document deduplication — acceptable
for Day 2's one-shot ingest; Phase 1 will replace this with proper incremental indexing.

Idempotency: Running the same operation multiple times produces the same end state as running it once.
"""
import argparse
import json
from pathlib import Path

from opensearchpy import OpenSearch, helpers

CHUNKS_DIR = Path("data/chunks")

MAPPING = {
    "mappings": {
        "properties": {
            "video_id": {"type": "keyword"},
            "title":    {"type": "text", "analyzer": "standard"},
            "start_ts": {"type": "float"},
            "end_ts":   {"type": "float"},
            "text":     {"type": "text", "analyzer": "standard"},
        }
    }
}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--index", default="chunks")
    p.add_argument("--host", default="localhost")
    p.add_argument("--port", type=int, default=9200)
    args = p.parse_args()

    client = OpenSearch(
        hosts=[{"host": args.host, "port": args.port}],
        use_ssl=False,
        verify_certs=False,
    )

    if client.indices.exists(index=args.index):
        print(f"dropping existing index '{args.index}'")
        client.indices.delete(index=args.index)

    client.indices.create(index=args.index, body=MAPPING)
    print(f"created index '{args.index}'")

    def gen():
        for path in sorted(CHUNKS_DIR.glob("*.jsonl")):
            for line in path.read_text().splitlines():
                chunk = json.loads(line)
                yield {"_index": args.index, "_source": chunk}

    # helpers.bulk: the efficient way to load many documents — it batches them into bulk HTTP requests under the hood
    # (success_count, errors)
    n, _ = helpers.bulk(client, gen())

    # OpenSearch doesn't make newly-indexed documents searchable immediately — it batches them for efficiency.
    # `refresh` forces this to happen now.
    # Without it, a query run immediately after indexing might return zero hits.
    client.indices.refresh(index=args.index)
    print(f"indexed {n} chunks")


if __name__ == "__main__":
    main()