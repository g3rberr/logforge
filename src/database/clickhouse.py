import asyncio
import logging
from typing import Any

from clickhouse_driver import Client as _CHClient

from core.config import settings

logger = logging.getLogger(__name__)


class ClickHouseClient:
    def __init__(self):
        self._client: Any = None

    def connect(self):
        self._client = _CHClient(
            host=settings.clickhouse_host,
            port=settings.clickhouse_port,
            user=settings.clickhouse_user,
            password=settings.clickhouse_password,
            database=settings.clickhouse_database,
        )
        logger.info("connected to clickhouse")

    def close(self):
        if self._client:
            self._client.disconnect()
            self._client = None

    @property
    def client(self):
        if self._client is None:
            raise RuntimeError("ClickHouse not connected")
        return self._client

    async def execute(
        self, query: str, params: dict[str, Any] | None = None
    ) -> list[dict[str, Any]]:
        result = await asyncio.to_thread(
            self.client.execute, query, params or {}, with_column_types=True
        )
        columns = [col[0] for col in result[0]]
        return [dict(zip(columns, row, strict=True)) for row in result[1]]

    async def insert(self, table: str, data: list[dict[str, Any]]) -> None:
        if not data:
            return
        columns = list(data[0].keys())
        rows = [[row[col] for col in columns] for row in data]
        await asyncio.to_thread(
            self.client.execute,
            f"INSERT INTO {table} ({', '.join(columns)}) VALUES",
            rows,
        )


ch_client = ClickHouseClient()
