from typing import Any

from database.clickhouse import ClickHouseClient
from models.clickhouse_models import LogEntry
from repositories.log import LogRepository
from schemas.log import LogEntryFilters, LogEntryStats


class AnalyticsService:
    def __init__(self, ch: ClickHouseClient) -> None:
        self._repo = LogRepository(ch)

    def ingest(self, project_id: str, entries: list[LogEntry]) -> None:
        self._repo.insert_batch(entries)

    def search(self, project_id: str, filters: LogEntryFilters) -> tuple[list[dict[str, Any]], int]:
        return self._repo.search(
            project_id,
            level=filters.level,
            source=filters.source,
            from_date=filters.from_date,
            to_date=filters.to_date,
            search=filters.search,
            limit=filters.limit,
            offset=filters.offset,
        )

    def stats(self, project_id: str, filters: LogEntryFilters) -> LogEntryStats:
        raw = self._repo.get_stats(
            project_id,
            from_date=filters.from_date,
            to_date=filters.to_date,
        )
        return LogEntryStats(
            total=raw["total"],
            by_level=raw["by_level"],
            from_date=filters.from_date,
            to_date=filters.to_date,
        )
