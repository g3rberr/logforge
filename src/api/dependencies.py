# ruff: noqa: B008
from collections.abc import AsyncGenerator

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.security import decode_token
from database.clickhouse import ClickHouseClient, ch_client
from database.postgres import get_session as _get_session
from models.postgres_models import User

get_session = _get_session

security = HTTPBearer(auto_error=False)


async def get_ch() -> AsyncGenerator[ClickHouseClient, None]:
    yield ch_client


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
    session: AsyncSession = Depends(get_session),
) -> User:
    if credentials is None:
        raise HTTPException(status_code=401, detail="invalid token format")
    user_id = decode_token(credentials.credentials)
    if user_id is None:
        raise HTTPException(status_code=401, detail="invalid or expired token")
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=401, detail="user not found")
    return user
