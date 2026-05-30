import logging
from typing import Any

from clickhouse_driver import Client as _CHClient

from core.config import settings

logger = logging.getLogger(__name__)


class ClickHouseClient:
    def __init__(self) -> None:
        self._client: Any = None

    def connect(self) -> None:
        self._client = _CHClient(
            host=settings.clickhouse_host,
            port=settings.clickhouse_port,
            user=settings.clickhouse_user,
            password=settings.clickhouse_password,
            database=settings.clickhouse_database,
        )
        logger.info("connected to clickhouse")

    def close(self) -> None:
        if self._client:
            self._client.disconnect()
            self._client = None

    @property
    def client(self) -> Any:  # noqa: ANN401
        if self._client is None:
            raise RuntimeError("ClickHouse not connected")
        return self._client

    def execute(self, query: str, params: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        result = self.client.execute(query, params or {}, with_column_types=True)
        columns = [col[0] for col in result[0]]
        return [dict(zip(columns, row, strict=False)) for row in result[1]]

    def insert(self, table: str, data: list[dict[str, Any]]) -> None:
        if not data:
            return
        columns = list(data[0].keys())
        rows = [[row[col] for col in columns] for row in data]
        self.client.execute(f"INSERT INTO {table} ({', '.join(columns)}) VALUES", rows)


ch_client = ClickHouseClient()
