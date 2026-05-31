from pydantic_settings import BaseSettings, SettingsConfigDict


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
