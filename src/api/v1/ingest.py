import json

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import get_ch, get_session
from database.clickhouse import ClickHouseClient
from models.clickhouse_models import LogEntry
from models.postgres_models import Project
from schemas.log import LogEntryCreate, LogEntryRead

router = APIRouter(prefix="/ingest", tags=["ingest"])


@router.post("", response_model=LogEntryRead, status_code=201)
async def ingest(
    data: LogEntryCreate,
    x_api_key: str = Header(...),
    session: AsyncSession = Depends(get_session),
    ch: ClickHouseClient = Depends(get_ch),
):
    result = await session.execute(select(Project).where(Project.api_key == x_api_key))
    project = result.scalar_one_or_none()
    if project is None:
        raise HTTPException(status_code=401, detail="invalid api key")

    entry = LogEntry(
        project_id=project.id,
        level=data.level,
        message=data.message,
        source=data.source,
        metadata=data.metadata,
        traceback=data.traceback,
        timestamp=data.timestamp,
    )

    row = entry.to_dict()
    row["metadata"] = json.dumps(row["metadata"])
    await ch.insert(LogEntry.__table__, [row])

    return LogEntryRead(
        id=entry.id,
        project_id=entry.project_id,
        source=entry.source,
        level=entry.level,
        message=entry.message,
        metadata=entry.metadata,
        traceback=entry.traceback,
        timestamp=entry.timestamp,
    )
