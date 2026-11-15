from functools import lru_cache
from pathlib import Path

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ROOT / ".env", extra="ignore")
    database_url: str = (
        "postgresql+psycopg://semi:local-only-change-me@127.0.0.1:55432/semiconductor"
    )
    storage_root: Path = ROOT / "data/raw"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    embedding_revision: str = "1110a243fdf4706b3f48f1d95db1a4f5529b4d41"
    model_directory: Path = ROOT / "models/minilm"
    llm_provider: str = "groq"
    llm_model: str | None = None
    groq_api_key: SecretStr | None = None
    enable_live_llm: bool = False
    sec_user_agent: str | None = None
    api_origins: list[str] = ["http://127.0.0.1:3100", "http://localhost:3100"]
    max_question_chars: int = 1200
    max_output_tokens: int = Field(default=600, ge=100, le=1000)


@lru_cache
def settings():
    return Settings()
