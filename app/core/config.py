# app/core/config.py
from __future__ import annotations

from functools import lru_cache
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Service identity
    service_name: str = "my-fastapi-service"
    version: str = "0.1.0"
    debug: bool = False

    # API
    api_prefix: str = "/api"
    enable_docs: bool = True

    # CORS
    # Example env: CORS_ORIGINS='["http://localhost:3000","https://example.com"]'
    cors_origins: List[str] = Field(default_factory=list)

    # Auth/security (optional baseline)
    jwt_secret: str = Field(default="change-me", repr=False)
    jwt_algorithm: str = "HS256"
    access_token_exp_minutes: int = 60

    # Database (optional baseline)
    database_url: str | None = None

    # Logging
    log_level: str = "INFO"
    json_logs: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    # Cached so imports are cheap and consistent
    return Settings()


settings = get_settings()