from collections.abc import AsyncGenerator

from fastapi import Depends, Header, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.security import decode_token
from database.clickhouse import ClickHouseClient, ch_client
from database.postgres import get_session as _get_session
from models.postgres_models import User

get_session = _get_session


async def get_ch() -> AsyncGenerator[ClickHouseClient, None]:
    yield ch_client


async def get_current_user(
    authorization: str = Header(...),
    session: AsyncSession = Depends(get_session),
) -> User:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="invalid token format")

    token = authorization.removeprefix("Bearer ")
    user_id = decode_token(token)
    if user_id is None:
        raise HTTPException(status_code=401, detail="invalid or expired token")

    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=401, detail="user not found")

    return user
