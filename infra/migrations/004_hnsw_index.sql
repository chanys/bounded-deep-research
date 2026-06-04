-- HNSW index for the production dense (pgvector) retrieval path.
--
-- ORDER MATTERS: run this AFTER the embed job has repopulated 1536-dim vectors
-- (load-then-index). Building HNSW on an empty/partly-loaded table is slower and
-- pointless; bulk-load first, index after, then ANALYZE.
--
-- 1536 < pgvector's 2000-dim HNSW cap, so a plain `vector` column with
-- `vector_cosine_ops` works directly (no halfvec). Cosine distance is correct
-- because both corpus and query vectors are L2-normalized (the dimensions=1536
-- API output is already normalized).

BEGIN;

CREATE INDEX IF NOT EXISTS idx_video_chunks_embedding_hnsw
    ON video_chunks USING hnsw (embedding vector_cosine_ops);

INSERT INTO schema_migrations (version) VALUES ('004_hnsw_index');

COMMIT;

-- ANALYZE outside the transaction so the planner has fresh stats for the new index.
ANALYZE video_chunks;
