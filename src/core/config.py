"""Application configuration via environment variables."""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Pydantic-based settings loaded from .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "logforge"
    app_version: str = "0.1.0"
    debug: bool = False

    postgres_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/logforge"
    postgres_echo: bool = False

    clickhouse_host: str = "localhost"
    clickhouse_port: int = 9000
    clickhouse_user: str = "default"
    clickhouse_password: str = ""
    clickhouse_database: str = "logforge"

    redis_url: str = "redis://localhost:6379/0"

    jwt_secret: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 1440

    api_prefix: str = "/api/v1"
    cors_origins: list[str] = ["*"]

    log_level: str = "INFO"


BASE_DIR = Path(__file__).resolve().parent.parent.parent
settings = Settings()
