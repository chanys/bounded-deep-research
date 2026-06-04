-- Re-embed the corpus at 1536 dimensions (Matryoshka-reduced text-embedding-3-large).
--
-- Why: pgvector's HNSW index caps at 2000 dims for the `vector` type, but the corpus
-- was originally embedded at the model's native 3072. Rather than carry halfvec in
-- production, we standardize on 1536 everywhere (config.embedding_dimensions), which
-- keeps a plain `vector` + standard `vector_cosine_ops` HNSW (migration 004) and is
-- well above where recall degrades for this corpus size.
--
-- This migration only resets state; the actual vectors are repopulated by the embed
-- job, which claims rows WHERE embedded_at IS NULL and now requests dimensions=1536.
-- Drop+add (rather than ALTER TYPE) sidesteps pgvector's typmod cast strictness.

BEGIN;

ALTER TABLE video_chunks DROP COLUMN embedding;
ALTER TABLE video_chunks ADD COLUMN embedding vector(1536);

-- Reset provenance so the embed job re-claims every chunk. The partial index
-- idx_video_chunks_unembedded (WHERE embedded_at IS NULL) auto-repopulates.
UPDATE video_chunks SET embedded_at = NULL, embedding_model = NULL;

INSERT INTO schema_migrations (version) VALUES ('003_embedding_1536');

COMMIT;
