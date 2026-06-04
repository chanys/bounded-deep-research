"""Embed chunks using OpenAI text-embedding-3-large. Postgres-driven.

Usage:
  uv run python -m ingest.embed_chunks --batch 1024
"""
import argparse

from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential
from tqdm import tqdm

from app.config import settings
from app.db import transaction

EMBEDDING_MODEL = settings.embedding_model
EMBEDDING_DIMENSIONS = settings.embedding_dimensions

client = OpenAI(api_key=settings.openai_api_key)


# The exponential wait is: multiplier × 2^(attempt-1), clamped at [2, 30] seconds range
# 2^(1-1)=2^0=2 (clamped at min=2) , 2^(2-1)=2^1=2 , 2^(3-1)=2^2=4 , 2^(4-1)=2^3=8 , 2^(5-1)=2^4=16
@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=2, max=30),
)
def embed_batch(texts: list[str]) -> list[list[float]]:
    resp = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=texts,
        dimensions=EMBEDDING_DIMENSIONS,  # Matryoshka-reduced; must match the query embedder
    )
    return [d.embedding for d in resp.data]


def fetch_batch(conn, batch_size: int) -> list[dict]:
    """
    What makes this progress through the batches one-by-one.
    After each batch is fetched and embedded successfully, the UPDATE sets embedded_at = NOW() on those 1024 rows.
    Now they no longer match WHERE embedded_at IS NULL.
    So the next time you run fetch_batch, those rows are gone from the result set.
    Hence Postgres returns the next 1024 unembedded chunks.

    Why ORDER BY video_id, start_s. : Deterministic batch order.
    If batch 17 crashes, batch 17 next run contains the same chunks -> debuggable.
    Without ORDER BY, Postgres makes no guarantees and every run shuffles.
    """
    return conn.execute("""
        SELECT chunk_id, text FROM video_chunks
        WHERE embedded_at IS NULL
        ORDER BY video_id, start_s
        LIMIT %s
    """, (batch_size,)).fetchall()


def count_remaining(conn) -> int:
    return conn.execute(
        "SELECT COUNT(*) AS n FROM video_chunks WHERE embedded_at IS NULL"
    ).fetchone()["n"]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--batch", type=int, default=1024)
    args = p.parse_args()

    with transaction() as conn:
        total = count_remaining(conn)

    if total == 0:
        print("nothing to embed")
        return

    print(f"embedding {total} chunks with {EMBEDDING_MODEL} "
          f"({EMBEDDING_DIMENSIONS} dims, batch={args.batch})")

    pbar = tqdm(total=total, desc="embedding")
    while True:
        # Why fetch_batch and the UPDATE share one transaction.
        # They're a single unit of work: "claim these N chunks, embed them, mark them done."
        #
        # **** IMPORTANT ****
        # `with transaction() as conn`: wraps the block in a transaction that commits on exit and rolls back on exception.
        # If you put `with transaction()` outside the `True` loop, you'd have one giant transaction covering all 25 batches.
        #
        # **The rule**: a transaction's boundaries should match the boundaries of the work you want to be atomic.
        # Embedding and marking-as-done is one atomic unit.
        with transaction() as conn:
            rows = fetch_batch(conn, args.batch)
            if not rows:
                break

            chunk_ids = [r["chunk_id"] for r in rows]
            texts = [r["text"] for r in rows]
            vectors = embed_batch(texts)

            updates = [
                (vec, EMBEDDING_MODEL, cid)
                for cid, vec in zip(chunk_ids, vectors)
            ]
            with conn.cursor() as cur:
                cur.executemany("""
                    UPDATE video_chunks
                    SET embedding = %s,
                        embedding_model = %s,
                        embedded_at = NOW()
                    WHERE chunk_id = %s
                """, updates)

            pbar.update(len(rows))

    pbar.close()
    print(f"done: {total} chunks embedded")


if __name__ == "__main__":
    main()