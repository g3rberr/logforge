from fastapi import APIRouter, Depends

from api.dependencies import get_current_user
from models.postgres_models import User
from schemas.user import UserRead

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserRead)
async def get_me(
    user: User = Depends(get_current_user),  # noqa: B008
) -> UserRead:
    return UserRead(
        id=user.id,
        email=user.email,
        name=user.name,
        created_at=user.created_at,
    )
