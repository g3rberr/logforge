from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import get_ch, get_current_user, get_session
from database.clickhouse import ClickHouseClient
from models.postgres_models import Project, User
from schemas.log import LogEntryFilters, LogEntryRead, LogEntryStats
from services.analytics_service import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/logs", response_model=list[LogEntryRead])
async def search_logs(
    project_id: str = Query(...),
    level: str | None = None,
    source: str | None = None,
    search: str | None = None,
    limit: int = Query(50, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_user),  # noqa: B008
    session: AsyncSession = Depends(get_session),  # noqa: B008
    ch: ClickHouseClient = Depends(get_ch),  # noqa: B008
) -> list[LogEntryRead]:
    result = await session.execute(
        select(Project).where(Project.id == project_id, Project.owner_id == current_user.id)
    )
    if result.scalar_one_or_none() is None:
        raise HTTPException(status_code=404, detail="project not found")

    filters = LogEntryFilters(level=level, source=source, search=search, limit=limit, offset=offset)
    service = AnalyticsService(ch)
    items, _ = service.search(project_id, filters)
    return [LogEntryRead(**item) for item in items]


@router.get("/stats", response_model=LogEntryStats)
async def get_stats(
    project_id: str = Query(...),
    current_user: User = Depends(get_current_user),  # noqa: B008
    session: AsyncSession = Depends(get_session),  # noqa: B008
    ch: ClickHouseClient = Depends(get_ch),  # noqa: B008
) -> LogEntryStats:
    result = await session.execute(
        select(Project).where(Project.id == project_id, Project.owner_id == current_user.id)
    )
    if result.scalar_one_or_none() is None:
        raise HTTPException(status_code=404, detail="project not found")

    service = AnalyticsService(ch)
    return service.stats(project_id, LogEntryFilters())
