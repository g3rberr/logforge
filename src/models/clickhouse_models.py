from datetime import UTC, datetime
from uuid import uuid4


class LogEntry:
    __table__ = "log_entries"

    def __init__(
        self,
        project_id: str,
        level: str,
        message: str,
        source: str = "api",
        metadata: dict[str, object] | None = None,
        traceback: str | None = None,
        timestamp: datetime | None = None,
    ) -> None:
        self.id = str(uuid4())
        self.project_id = project_id
        self.source = source
        self.level = level
        self.message = message
        self.metadata = metadata or {}
        self.traceback = traceback or ""
        self.timestamp = timestamp or datetime.now(UTC)

    def to_dict(self) -> dict[str, object]:
        return {
            "id": self.id,
            "project_id": self.project_id,
            "source": self.source,
            "level": self.level,
            "message": self.message,
            "metadata": self.metadata,
            "traceback": self.traceback,
            "timestamp": self.timestamp,
        }
