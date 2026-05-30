import json
from datetime import datetime
from typing import Any

from database.clickhouse import ClickHouseClient
from models.clickhouse_models import LogEntry


class LogRepository:
    def __init__(self, ch: ClickHouseClient) -> None:
        self._ch = ch

    def insert_batch(self, entries: list[LogEntry]) -> None:
        data = []
        for e in entries:
            record = e.to_dict()
            record["metadata"] = json.dumps(record["metadata"])
            data.append(record)
        self._ch.insert(LogEntry.__table__, data)

    def search(
        self,
        project_id: str,
        level: str | None = None,
        source: str | None = None,
        from_date: datetime | None = None,
        to_date: datetime | None = None,
        search: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> tuple[list[dict[str, Any]], int]:
        conditions = ["project_id = %(project_id)s"]
        params: dict[str, Any] = {"project_id": project_id}

        if level:
            conditions.append("level = %(level)s")
            params["level"] = level
        if source:
            conditions.append("source = %(source)s")
            params["source"] = source
        if from_date:
            conditions.append("timestamp >= %(from_date)s")
            params["from_date"] = from_date
        if to_date:
            conditions.append("timestamp <= %(to_date)s")
            params["to_date"] = to_date
        if search:
            conditions.append("(message LIKE %(search)s OR traceback LIKE %(search)s)")
            params["search"] = f"%{search}%"

        where = " AND ".join(conditions)

        count_result = self._ch.execute(
            f"SELECT count() as cnt FROM {LogEntry.__table__} WHERE {where}", params
        )
        total = count_result[0]["cnt"] if count_result else 0

        rows = self._ch.execute(
            f"SELECT * FROM {LogEntry.__table__} WHERE {where} "
            f"ORDER BY timestamp DESC LIMIT %(limit)s OFFSET %(offset)s",
            {**params, "limit": limit, "offset": offset},
        )

        items = []
        for row in rows:
            if isinstance(row.get("metadata"), str):
                row["metadata"] = json.loads(row["metadata"])
            items.append(row)

        return items, total

    def get_stats(
        self,
        project_id: str,
        from_date: datetime | None = None,
        to_date: datetime | None = None,
    ) -> dict[str, Any]:
        conditions = ["project_id = %(project_id)s"]
        params: dict[str, Any] = {"project_id": project_id}

        if from_date:
            conditions.append("timestamp >= %(from_date)s")
            params["from_date"] = from_date
        if to_date:
            conditions.append("timestamp <= %(to_date)s")
            params["to_date"] = to_date

        where = " AND ".join(conditions)

        total = self._ch.execute(
            f"SELECT count() as cnt FROM {LogEntry.__table__} WHERE {where}", params
        )[0]["cnt"]

        by_level = self._ch.execute(
            f"SELECT level, count() as cnt FROM {LogEntry.__table__} WHERE {where} GROUP BY level",
            params,
        )
        return {"total": total, "by_level": {r["level"]: r["cnt"] for r in by_level}}
