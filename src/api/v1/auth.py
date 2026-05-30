from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import get_session
from schemas.user import TokenResponse, UserCreate, UserLogin, UserRead
from services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=201)
async def register(data: UserCreate, session: AsyncSession = Depends(get_session)) -> UserRead:  # noqa: B008
    service = AuthService(session)
    try:
        user = await service.register(data)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e)) from e
    return UserRead(
        id=user.id,
        email=user.email,
        name=user.name,
        created_at=user.created_at,
    )


@router.post("/login", response_model=TokenResponse)
async def login(data: UserLogin, session: AsyncSession = Depends(get_session)) -> TokenResponse:  # noqa: B008
    service = AuthService(session)
    try:
        token = await service.login(data.email, data.password)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e)) from e
    return TokenResponse(access_token=token)
