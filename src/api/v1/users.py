from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import get_current_user, get_session
from core.security import hash_password
from models.postgres_models import User
from schemas.user import UserRead, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserRead)
async def get_me(
    user: User = Depends(get_current_user),
):
    return UserRead(
        id=user.id,
        email=user.email,
        name=user.name,
        created_at=user.created_at,
    )


@router.put("/me", response_model=UserRead)
async def update_me(
    data: UserUpdate,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    if data.name is not None:
        user.name = data.name
    if data.password is not None:
        user.hashed_password = hash_password(data.password)
    session.add(user)
    await session.flush()
    await session.refresh(user)
    return UserRead(
        id=user.id,
        email=user.email,
        name=user.name,
        created_at=user.created_at,
    )
