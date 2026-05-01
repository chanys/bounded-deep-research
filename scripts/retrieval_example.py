from app.retrieval import search

q = "what is graph rag"
ch = "code4AI"

bm25 = search(q, ch, k=10, mode="bm25")
dense = search(q, ch, k=10, mode="dense")
hybrid = search(q, ch, k=10, mode="hybrid")

for label, hits in [("bm25", bm25), ("dense", dense), ("hybrid", hybrid)]:
    print(f"\n=== {label} ===")
    for h in hits[:5]:
        print(f"  {h['score']:.4f}  {h['video_id']}  {h['title'][:50]}")
