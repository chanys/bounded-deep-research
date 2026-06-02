import asyncio

from app.retrieval import search

q = "what is graph rag"
ch = "code4AI"


async def main():
    bm25 = await search(q, ch, k=10, mode="bm25")
    dense = await search(q, ch, k=10, mode="dense")
    hybrid = await search(q, ch, k=10, mode="hybrid")

    for label, hits in [("bm25", bm25), ("dense", dense), ("hybrid", hybrid)]:
        print(f"\n=== {label} ===")
        for h in hits[:5]:
            print(f"  {h['score']:.4f}  {h['chunk_id']}  {h['title'][:40]}")
            print(f"    {h['text'][:200]}")


if __name__ == "__main__":
    asyncio.run(main())
