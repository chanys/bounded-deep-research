"""Retrieval over indexed transcript chunks. Three modes: bm25, dense, hybrid."""
import asyncio
from typing import Literal

from openai import AsyncOpenAI
from opensearchpy import AsyncOpenSearch

from app.config import settings

Mode = Literal["bm25", "dense", "hybrid"]

EMBEDDING_MODEL = settings.embedding_model

_client = AsyncOpenSearch(
    hosts=[{"host": "localhost", "port": 9200}],
    use_ssl=False,
    verify_certs=False,
)

_openai_client = AsyncOpenAI(api_key=settings.openai_api_key)


async def aclose() -> None:
    """Close the async OpenSearch client's aiohttp session. Call on shutdown.

    AsyncOpenSearch holds an aiohttp ClientSession that, unlike the old sync
    client, must be closed explicitly or aiohttp warns at interpreter exit.
    """
    await _client.close()


def _index_for(channel: str) -> str:
    return f"{settings.opensearch_index_prefix}_{channel}".lower()


async def _embed_query(query: str) -> list[float]:
    """Embed a single query for dense retrieval. Same model as the corpus."""
    resp = await _openai_client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=[query],
        dimensions=settings.embedding_dimensions,  # must match the corpus embed job
    )
    return resp.data[0].embedding


def _doc_key(hit: dict) -> str:
    """Stable key for a chunk across rankers."""
    return f"{hit['video_id']}:{hit['start_ts']}"


async def chunk_exists(video_id: str, start_ts: int, channel: str) -> bool:
    """Check whether a chunk with exact (video_id, start_ts) exists.
    size: 1        # we only need to know whether any exists
    bool + filter  # combine multiple conditions with AND
    """
    body = {
        "size": 1,
        "query": {
            "bool": {
                "filter": [
                    {"term": {"video_id": video_id}},
                    {"term": {"start_ts": start_ts}},
                ]
            }
        },
    }
    res = await _client.search(index=_index_for(channel), body=body)
    return res["hits"]["total"]["value"] > 0


async def read_video_segment(video_id: str, start_ts: int, channel: str) -> dict | None:
    """Return the full chunk at (video_id, start_ts), or None if no match.
    """
    body = {
        "size": 1,
        "query": {
            "bool": {
                "filter": [
                    {"term": {"video_id": video_id}},
                    {"term": {"start_ts": start_ts}},
                ]
            }
        },
    }
    res = await _client.search(index=_index_for(channel), body=body)
    hits = res["hits"]["hits"]
    if not hits:
        return None
    source = hits[0]["_source"]

    return {
        "video_id": source["video_id"],
        "title": source["title"],
        "start_ts": source["start_ts"],
        "end_ts": source["end_ts"],
        "text": source["text"],
    }


async def search(
    query: str,
    channel: str,
    k: int = 10,
    mode: Mode = "hybrid",
) -> list[dict]:
    """Search transcripts. Returns list of {video_id, title, start_ts, end_ts, text, score}.

    Mode determines retrieval strategy:
    - bm25:   lexical match via OpenSearch BM25 against `text`
    - dense:  kNN over query embedding against `embedding`
    - hybrid: RRF over both rankings (default)

    Each hit is OpenSearch's wrapper around one matching document. Shape:
    {
        "_index": "chunks_code4ai",
        "_id": "<chunk_id>",
        "_score": 8.42,
        "_source": {
            "video_id": "...",
            "title": "...",
            "start_ts": 120,
            "end_ts": 150,
            "text": "...",
            ...
        }
    }
    We unpack _source and overwrite score with _score (or fused RRF score).
    """
    if mode == "bm25":
        return await _bm25_search(query, channel, k)
    if mode == "dense":
        return await _dense_search(query, channel, k)
    if mode == "hybrid":
        return await _hybrid_search(query, channel, k)
    raise ValueError(f"unknown mode: {mode}")


# ---------------------------------------------------------------------------
# Mode implementations
# ---------------------------------------------------------------------------


async def _bm25_search(query: str, channel: str, k: int) -> list[dict]:
    """BM25 search. Returns list of {video_id, title, start_ts, end_ts, text, score}.

    Each hit is OpenSearch's wrapper around one matching document. Shape:
    {
        "_index": "chunks",
        "_id": "abc123xyz",           # auto-generated doc id
        "_score": 8.42,                # BM25 score
        "_source": {                   # your original document
            "video_id": "DdakyHWTkRk",
            "title": "TEST KIMI K2.6 ...",
            "start_ts": 120.0,
            "end_ts": 150.0,
            "text": "..."
        }
    }

    _source is the chunk you indexed; everything else is OpenSearch metadata.

    ===================

    The ** is dict unpacking: it spreads a dict's key-value pairs into another dict literal.

    ```
    {**hit["_source"], "score": hit["_score"]}
    ```

    Equivalent to:
    ```
    {
        "video_id": hit["_source"]["video_id"],
        "title":    hit["_source"]["title"],
        "start_ts": hit["_source"]["start_ts"],
        "end_ts":   hit["_source"]["end_ts"],
        "text":     hit["_source"]["text"],
        "score":    hit["_score"],
    }
    ```

    fields: ["title^2.0", "text"] — title^2.0 means "match against title with weight 2.0".
            text (no ^) means weight 1.0.
            So a document scoring 5.0 on title alone would beat a document scoring 9.0 on text alone (5.0 × 2.0 = 10.0 > 9.0).

    type: "best_fields" -- when a query matches multiple fields, take the highest-scoring field's score (rather than summing across fields).
                           Best when you expect the query to match one field strongly.
          "most_fields" — sum across fields (rewards docs that match many fields a little)
    """
    resp = await _client.search(
        index=_index_for(channel),
        body={
            "size": k,
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": [
                        f"title^{settings.title_boost}",
                        "text",
                    ],
                    "type": "most_fields",
                }
            },
        },
    )
    return [
        {**hit["_source"], "score": hit["_score"]}
        for hit in resp["hits"]["hits"]
    ]


async def _dense_search(query: str, channel: str, k: int) -> list[dict]:
    """
    Worth understanding: the kNN query has two k values:
    - outer size (how many docs to return)
    - inner k (how many candidates the HNSW algorithm considers).

    Setting them equal is the simplest case.
    In production tuning you'd often set inner k higher (e.g., 100) to give HNSW more candidates to choose from, then return the top size.

    The production pattern (inner 100, outer 10) means:
    - "explore enough graph to be confident the true top-10 is in my candidate pool of 100, then return only the 10 best of those 100."
    """
    vec = await _embed_query(query)
    resp = await _client.search(
        index=_index_for(channel),
        body={
            "size": k,
            "query": {"knn": {"embedding": {"vector": vec, "k": k}}},
        },
    )
    return [
        {**hit["_source"], "score": hit["_score"]}
        for hit in resp["hits"]["hits"]
    ]


async def _hybrid_search(query: str, channel: str, k: int) -> list[dict]:
    """
    Why fetch more than k from each. RRF fuses ranks.
    If a doc is rank 1 in BM25 and rank 47 in dense, but you only fetched top-10 from dense, you'd never see rank 47.
    The doc gets full credit from BM25 only, missing the signal that dense also ranked it (if not highly).
    Fetching a wider pool gives RRF more material to work with.

    Why pool = 5*k or 50. Heuristic. Wider pools find more agreement signal at low cost.
    """
    # Fetch a wider pool from each ranker so RRF has agreement signal to work with.
    # The two rankers are independent, so run them concurrently: wall-clock is the
    # slower of the two, not their sum.
    pool = max(k * 5, 50)
    bm25_hits, dense_hits = await asyncio.gather(
        _bm25_search(query, channel, pool),
        _dense_search(query, channel, pool),
    )
    return _rrf_fuse(bm25_hits, dense_hits, k=k, rrf_k=60)


# ---------------------------------------------------------------------------
# Reciprocal Rank Fusion
# ---------------------------------------------------------------------------

# REF: https://opensearch.org/blog/introducing-reciprocal-rank-fusion-hybrid-search/
# REF: https://blog.serghei.pl/posts/reciprocal-rank-fusion-explained/
def _rrf_fuse(
    bm25_hits: list[dict],
    dense_hits: list[dict],
    k: int,
    rrf_k: int = 60,
) -> list[dict]:
    r"""Reciprocal Rank Fusion. score(doc) = sum over rankers of 1 / (rrf_k + rank).

    RRFscore(d) = \sum_{r \in R} frac{1}{k + r(d)}
    where r(d) is the rank of document d in ranker r's list, and k=60 is a constant from the original 2009 paper.

    rrf_k=60 is the value from Cormack et al. 2009; default everywhere.

    Returns top-k docs by fused score. Each doc keeps the metadata from
    whichever ranker saw it first (BM25 takes precedence). The `score`
    field is replaced with the fused RRF score.

    ==============

    The formula. For each ranker that returned the doc, contribute 1 / (rrf_k + rank).
    So a doc at rank 1 in BM25 and rank 1 in dense gets 1/61 + 1/61 ≈ 0.033.
    A doc at rank 1 in only one ranker gets 1/61 ≈ 0.016.
    A doc at rank 100 in both gets 2/160 ≈ 0.013.
    The constant rrf_k = 60 is the value from the original RRF paper (Cormack et al. 2009) and the default everywhere; don't change it without a reason.

    Why this formula and not score-weighted averaging?
    BM25 scores and kNN scores are on different scales — BM25 is unbounded ("8.42"), cosine similarity is bounded ([0,1]).
    Averaging them requires normalization, normalization is hand-wavy, and the combined score becomes sensitive to which side has more variance.
    RRF sidesteps this by using only ranks. Robust, stable, requires no tuning.

    Why preferring BM25 metadata when both rankers see a doc.
    Both should have identical _source (it's the same OpenSearch index),
    but in case of any subtle difference, picking deterministically keeps results reproducible across runs.

    Why dict + setdefault instead of building a fancy structure.
    Two passes, simple. Easy to understand. ~10 lines as promised.
    """
    # rank is 1-indexed
    bm25_ranks = {_doc_key(h): i + 1 for i, h in enumerate(bm25_hits)}
    dense_ranks = {_doc_key(h): i + 1 for i, h in enumerate(dense_hits)}

    # Collect every doc seen by either ranker, BM25 source preferred.
    by_key: dict[str, dict] = {}
    for h in bm25_hits:
        by_key[_doc_key(h)] = h
    for h in dense_hits:
        by_key.setdefault(_doc_key(h), h)  # setdefault(key, value): if key already in dict, leave it alone. Else set it to value

    scored = []
    for key, hit in by_key.items():
        score = 0.0
        if key in bm25_ranks:
            score += 1.0 / (rrf_k + bm25_ranks[key])
        if key in dense_ranks:
            score += 1.0 / (rrf_k + dense_ranks[key])
        scored.append({**hit, "score": score})

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:k]