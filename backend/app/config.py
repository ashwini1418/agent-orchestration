# BACKEND_AGENT | 2026-05-10 | Pydantic Settings - reads all config from environment
from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    anthropic_api_key: str = ""
    database_url: str = "sqlite+aiosqlite:///./data/jobs.db"
    output_dir: str = "./output"

    jwt_private_key_path: str = "./keys/private.pem"
    jwt_public_key_path: str = "./keys/public.pem"
    jwt_algorithm: str = "RS256"
    jwt_expire_minutes: int = 1440

    allowed_origins: list[str] = ["http://localhost:5173", "http://localhost:3000"]
    max_sessions_per_user: int = 2
    api_semaphore_limit: int = 3

    debug: bool = False


settings = Settings()
