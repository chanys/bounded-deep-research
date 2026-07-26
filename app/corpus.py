"""Corpus identity: a stable fingerprint of the local index a run searched.

Stamped into RunProvenance so the same question/gold/judge stays re-interpretable
as the corpus grows. The identity covers the *retrievable* corpus (videos that
have chunks), described by four counts plus a content hash:
`<channel>:v<videos>:c<chunks>:<latest_publish_date>:<sha12>`, where sha12 is the
first 12 hex of SHA-1 over the channel's sorted chunk_ids and catches any content
change the counts alone would miss.

Computed once per channel per process and cached: ingestion is offline, so the
corpus never changes within a running process, and this otherwise scans every
chunk_id on each agent run (including every production /query).
"""
from __future__ import annotations

import hashlib
from functools import lru_cache

from core.db import transaction


@lru_cache(maxsize=None)
def corpus_id(channel: str) -> str:
    """Return the fingerprint of `channel`'s retrievable corpus in the local index.

    Ties video count and latest publish date to the same chunked set the SHA
    covers, so all four fields describe one consistent corpus. Raises if the DB is
    down; a run must not be stamped with an unknown corpus, and the query itself
    needs the DB anyway, so this adds no new failure mode.
    """
    chunks_sql = (
        "SELECT c.chunk_id FROM video_chunks c JOIN videos v USING (video_id) "
        "WHERE v.channel = %s ORDER BY c.chunk_id"
    )
    meta_sql = (
        "SELECT COUNT(DISTINCT c.video_id) AS videos, MAX(v.published_at) AS max_pub "
        "FROM video_chunks c JOIN videos v USING (video_id) WHERE v.channel = %s"
    )
    with transaction() as conn:
        chunk_ids = [r["chunk_id"] for r in conn.execute(chunks_sql, (channel,)).fetchall()]
        meta = conn.execute(meta_sql, (channel,)).fetchone()

    sha = hashlib.sha1("\n".join(chunk_ids).encode()).hexdigest()[:12]
    max_pub = meta["max_pub"]
    max_pub_str = max_pub.date().isoformat() if max_pub else "none"
    return f"{channel}:v{meta['videos']}:c{len(chunk_ids)}:{max_pub_str}:{sha}"
