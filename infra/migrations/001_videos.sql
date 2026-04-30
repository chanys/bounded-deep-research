CREATE TYPE video_status AS ENUM ('pending', 'fetched', 'failed', 'excluded');

CREATE TABLE videos (
    video_id TEXT PRIMARY KEY,
    channel TEXT NOT NULL,

    -- YouTube metadata (from channel manifest)
    title TEXT,
    published_at TIMESTAMPTZ,
    duration_s INTEGER,

    -- Status & exclusion
    status video_status NOT NULL DEFAULT 'pending',
    fetch_error TEXT,
    excluded_reason TEXT,

    -- Transcript
    transcript_language TEXT,
    transcript_is_generated BOOLEAN,
    transcript_n_segments INTEGER,
    fetched_at TIMESTAMPTZ,

    -- Cleanup
    cleanup_model TEXT,
    cleanup_prompt_version TEXT,
    cleaned_at TIMESTAMPTZ,

    -- Chunking
    chunk_window_s INTEGER,
    n_chunks INTEGER,
    chunked_at TIMESTAMPTZ,

    -- Embeddings
    embedding_model TEXT,
    embedded_at TIMESTAMPTZ,

    -- Index
    indexed_at TIMESTAMPTZ
);

CREATE INDEX ON videos (channel, status);
