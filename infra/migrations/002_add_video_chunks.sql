BEGIN;

-- 1. Enable pgvector
CREATE EXTENSION IF NOT EXISTS vector;

-- 2. Create video_chunks table (3NF — no denormalized title/channel/published_at)
CREATE TABLE IF NOT EXISTS video_chunks (
    chunk_id        TEXT PRIMARY KEY,
    video_id        TEXT NOT NULL REFERENCES videos(video_id) ON DELETE CASCADE,
    start_s         INTEGER NOT NULL,
    end_s           INTEGER NOT NULL,
    text            TEXT NOT NULL,
    embedding       vector(3072),
    embedding_model TEXT,
    embedded_at     TIMESTAMPTZ,
    CONSTRAINT video_chunks_span_valid CHECK (end_s > start_s)
);

CREATE INDEX IF NOT EXISTS idx_video_chunks_video_id ON video_chunks(video_id);
CREATE INDEX IF NOT EXISTS idx_video_chunks_unembedded
    ON video_chunks(video_id, start_s)
    WHERE embedded_at IS NULL;

-- 3. Drop the rollup column from videos (was: convenience flag, now derivable from video_chunks)
ALTER TABLE videos DROP COLUMN IF EXISTS embedded_at;
ALTER TABLE videos DROP COLUMN IF EXISTS embedding_model;

-- 4. Record the migration
CREATE TABLE IF NOT EXISTS schema_migrations (
    version    TEXT PRIMARY KEY,
    applied_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
INSERT INTO schema_migrations (version) VALUES ('002_add_video_chunks');

COMMIT;
