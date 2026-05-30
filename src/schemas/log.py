from datetime import datetime

from pydantic import BaseModel


class LogEntryCreate(BaseModel):
    source: str = "api"
    level: str = "INFO"
    message: str
    metadata: dict[str, object] | None = None
    traceback: str | None = None
    timestamp: datetime | None = None


class LogEntryRead(BaseModel):
    id: str
    project_id: str
    source: str
    level: str
    message: str
    metadata: dict[str, object]
    traceback: str
    timestamp: datetime


class LogEntryFilters(BaseModel):
    level: str | None = None
    source: str | None = None
    from_date: datetime | None = None
    to_date: datetime | None = None
    search: str | None = None
    limit: int = 50
    offset: int = 0


class LogEntryStats(BaseModel):
    total: int
    by_level: dict[str, int]
    from_date: datetime | None = None
    to_date: datetime | None = None
