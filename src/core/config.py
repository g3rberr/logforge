import logging

from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    postgres_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/logforge"
    clickhouse_host: str = "localhost"
    clickhouse_port: int = 9000
    clickhouse_user: str = "default"
    clickhouse_password: str = ""
    clickhouse_database: str = "logforge"
    jwt_secret: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 1440
    api_prefix: str = "/api/v1"
    cors_origins: list[str] = ["*"]
    debug: bool = False


settings = Settings()

if settings.jwt_secret == "change-me-in-production":
    logger.warning("jwt_secret is set to the default value; change it in production")
