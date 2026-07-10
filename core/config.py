from typing import Literal

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Precedence, highest to lowest:
    - Arguments passed directly to Settings(...)
    - Environment variables
    - The .env file
    - Field defaults
    """
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # your .env can have vars that don't correspond to any Settings field
    )

    # LLM
    openai_api_key: str
    agent_model: str = "gpt-5.4"
    reasoning_effort: str = "none"  # exploration turns (search / read)
    # Reasoning effort for the final synthesis (the submit_answer turn) only, where
    # reasoning helps answer quality. Exploration stays at `reasoning_effort`.
    synthesis_reasoning_effort: str = "low"
    # Reasoning summary: "auto" | "concise" | "detailed", or None to disable.
    # The API returns a summary of the reasoning, never the raw chain-of-thought.
    reasoning_summary: str | None = "auto"
    agent_max_steps: int = 15

    # Retrieval engine for `app/retrieval.py`. This selects the backend by *consumer*,
    # not by environment:
    # - "pgvector": used by the serving app (the /query endpoint). Dense-only kNN over
    #   the Postgres HNSW index; `mode` is forced to dense. This is the default so the
    #   app runs the SAME retrieval code everywhere (laptop and AWS) -> you test what
    #   you ship.
    # - "opensearch": selected (via env) only by the offline eval/ablation scripts,
    #   which need all three modes (bm25 / dense / hybrid). Never used to serve traffic.
    retrieval_backend: Literal["pgvector", "opensearch"] = "pgvector"
    retrieval_k: int = 10
    opensearch_url: str = "http://localhost:9200"
    opensearch_index_prefix: str = "chunks"
    embedding_model: str = "text-embedding-3-large"
    # text-embedding-3-large is natively 3072-dim. We request a Matryoshka-reduced
    # 1536 via the `dimensions` API param: still high quality (MRL prefix + L2 renorm)
    # while fitting under pgvector's 2000-dim HNSW limit for the production dense path.
    # This value must be passed to BOTH the corpus embed job and the query embedder so
    # stored vectors and query vectors share a space.
    embedding_dimensions: int = 1536
    title_boost: float = 1.0

    # Ingestion. Optional: only the offline ingest jobs need it. The serving app must
    # start without it (prod drops this secret), so it defaults to None.
    youtube_api_key: str | None = None

    # Observability
    langfuse_public_key: str | None = None
    langfuse_secret_key: str | None = None
    langfuse_base_url: str | None = None

    # Database. Locally we use DATABASE_URL directly (the default below). In production
    # the password arrives on its own (DB_PASSWORD, injected from a secret) and the rest
    # as plain env (DB_HOST etc.); we then assemble DATABASE_URL from the parts. Keeping
    # the password separate avoids ever splicing a secret into a URL string by hand.
    database_url: str = "postgresql://bdr:bdr_dev@localhost:5432/bdr"
    db_host: str | None = None
    db_port: int = 5432
    db_name: str = "bdr"
    db_user: str = "bdr"
    db_password: str | None = None

    # Cost controls. Two SEPARATE daily budgets, so a live demo can never be blocked by
    # (or block) public usage:
    daily_spend_cap_usd: float = 5.0   # PUBLIC budget (anonymous + access-code visitors)
    owner_spend_cap_usd: float = 25.0  # OWNER budget (the private demo code), kept apart

    # Access control. Two codes, both supplied via ?k= / the request body:
    # - access_code: on the resume; unlocks the higher per-IP quota, draws the public budget.
    # - owner_code:  private (your live demos); NO per-IP limit, draws the owner budget, so
    #                your demo is never blocked by public traffic and vice versa.
    access_code: str | None = None
    owner_code: str | None = None
    anon_daily_quota: int = 5    # queries per IP per day without a code
    coded_daily_quota: int = 50  # queries per IP per day with the access code

    @model_validator(mode="after")
    def _assemble_database_url(self):
        # Only override the default DATABASE_URL when the production parts are present.
        if self.db_host and self.db_password:
            self.database_url = (
                f"postgresql://{self.db_user}:{self.db_password}"
                f"@{self.db_host}:{self.db_port}/{self.db_name}"
            )
        return self

    # CORS: which browser origin(s) may call this API. Comma-separated.
    # Local dev = the Next dev server; prod = the deployed frontend domain
    # (set FRONTEND_ORIGIN=https://app.yeesengchan.com on AWS).
    frontend_origin: str = "http://localhost:3000"

    @property
    def cors_allow_origins(self) -> list[str]:
        return [o.strip() for o in self.frontend_origin.split(",") if o.strip()]


settings = Settings()


"""
Langfuse reads os.environ, not .env directly.
The above core.config.settings loads .env via pydantic-settings, 
but that loads into settings.langfuse_public_key, not into os.environ.
So when Langfuse's SDK looks at os.environ["LANGFUSE_PUBLIC_KEY"], it finds nothing.
So we add the following.
"""
import os
if settings.langfuse_public_key:
    os.environ["LANGFUSE_PUBLIC_KEY"] = settings.langfuse_public_key
if settings.langfuse_secret_key:
    os.environ["LANGFUSE_SECRET_KEY"] = settings.langfuse_secret_key
if settings.langfuse_base_url:
    os.environ["LANGFUSE_BASE_URL"] = settings.langfuse_base_url