"""
Validated environment configuration using Pydantic Settings.
All secrets come from environment variables — never hardcoded.
"""
from functools import lru_cache
from typing import Literal

from pydantic import AnyHttpUrl, Field, PostgresDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── Application ──────────────────────────────────────────────────────────
    NODE_ENV: Literal["development", "production", "test"] = "development"
    APP_NAME: str = "TaskFlow API"
    APP_VERSION: str = "1.0.0"
    PORT: int = 8000
    DEBUG: bool = False

    # ── Database ──────────────────────────────────────────────────────────────
    DATABASE_URL: str = Field(..., description="PostgreSQL async DSN")
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20

    # ── Redis ─────────────────────────────────────────────────────────────────
    REDIS_URL: str = Field(..., description="Redis connection URL")

    # ── JWT ───────────────────────────────────────────────────────────────────
    JWT_ACCESS_SECRET: str = Field(..., min_length=32)
    JWT_REFRESH_SECRET: str = Field(..., min_length=32)
    JWT_ACCESS_EXPIRE_MINUTES: int = 15
    JWT_REFRESH_EXPIRE_DAYS: int = 7

    # ── CORS ──────────────────────────────────────────────────────────────────
    CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://localhost:3000"]

    # ── OAuth ─────────────────────────────────────────────────────────────────
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GITHUB_CLIENT_ID: str = ""
    GITHUB_CLIENT_SECRET: str = ""
    OAUTH_REDIRECT_BASE_URL: str = "http://localhost:5173"

    # ── Email ─────────────────────────────────────────────────────────────────
    SMTP_HOST: str = "localhost"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM_EMAIL: str = "noreply@taskflow.app"
    SMTP_FROM_NAME: str = "TaskFlow"
    SENDGRID_API_KEY: str = ""
    EMAIL_PROVIDER: Literal["smtp", "sendgrid"] = "smtp"

    # ── AWS / S3 ──────────────────────────────────────────────────────────────
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_REGION: str = "us-east-1"
    AWS_S3_BUCKET: str = "taskflow-attachments"
    S3_ENDPOINT_URL: str = ""  # Empty = AWS, set for MinIO

    # ── OpenAI ────────────────────────────────────────────────────────────────
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o"
    OPENAI_MAX_TOKENS: int = 1000

    # ── Rate Limiting ─────────────────────────────────────────────────────────
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW_SECONDS: int = 60

    # ── Frontend ──────────────────────────────────────────────────────────────
    FRONTEND_URL: str = "http://localhost:5173"

    @field_validator("DATABASE_URL")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        if not v.startswith(("postgresql+asyncpg://", "postgresql://", "postgres://")):
            raise ValueError("DATABASE_URL must be a PostgreSQL connection string")
        # Normalize to asyncpg driver
        return v.replace("postgresql://", "postgresql+asyncpg://").replace(
            "postgres://", "postgresql+asyncpg://"
        )

    @property
    def is_production(self) -> bool:
        return self.NODE_ENV == "production"

    @property
    def is_development(self) -> bool:
        return self.NODE_ENV == "development"

    @property
    def is_test(self) -> bool:
        return self.NODE_ENV == "test"


@lru_cache
def get_settings() -> Settings:
    """Cached settings singleton — call this everywhere."""
    return Settings()


settings = get_settings()
