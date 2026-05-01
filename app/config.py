from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # your .env can have vars that don't correspond to any Settings field
    )

    # LLM
    openai_api_key: str
    agent_model: str = "gpt-5.4-mini"
    reasoning_effort: str = "medium"
    agent_max_steps: int = 15

    # Retrieval
    retrieval_k: int = 10
    opensearch_url: str = "http://localhost:9200"
    opensearch_index_prefix: str = "chunks"
    embedding_model: str = "text-embedding-3-large"
    embedding_dimensions: int = 3072

    # Ingestion
    youtube_api_key: str

    # Observability
    langfuse_public_key: str | None = None
    langfuse_secret_key: str | None = None
    langfuse_base_url: str | None = None

    # Database
    database_url: str = "postgresql://bdr:bdr_dev@localhost:5432/bdr"


settings = Settings()


"""
Langfuse reads os.environ, not .env directly.
The above app.config.settings loads .env via pydantic-settings, 
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