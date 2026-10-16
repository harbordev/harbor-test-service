from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration and Harbor deployment metadata."""

    APP_NAME: str = "Harbor FastAPI Test Service"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = False
    PORT: int = 8000
    ALLOWED_ORIGINS: List[str] = ["*"]

    # Harbor Integration Metadata
    HARBOR_PROJECT_ID: str | None = None
    HARBOR_SERVICE_ID: str | None = None
    HARBOR_DEPLOYMENT_ID: str | None = None
    HARBOR_ENVIRONMENT: str | None = None
    GIT_COMMIT_SHA: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
