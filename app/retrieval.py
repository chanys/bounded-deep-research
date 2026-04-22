"""BM25 search over indexed transcript chunks."""
from opensearchpy import OpenSearch

_client = OpenSearch(
    hosts=[{"host": "localhost", "port": 9200}],
    use_ssl=False,
    verify_certs=False,
)


def search(query: str, k: int = 10, index: str = "chunks") -> list[dict]:
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
    """
    resp = _client.search(
        index=index,
        body={
            "size": k,
            "query": {"match": {"text": query}},
        },
    )
    return [
        {**hit["_source"], "score": hit["_score"]}
        for hit in resp["hits"]["hits"]
    ]