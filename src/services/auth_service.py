from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.security import create_token, hash_password, verify_password
from models.postgres_models import User
from schemas.user import UserCreate


class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def register(self, data: UserCreate) -> User:
        existing = await self.session.execute(select(User).where(User.email == data.email))
        if existing.scalar_one_or_none() is not None:
            raise ValueError("email already taken")

        user = User(
            email=data.email,
            hashed_password=hash_password(data.password),
            name=data.name,
        )
        self.session.add(user)
        await self.session.flush()
        await self.session.refresh(user)
        return user

    async def login(self, email: str, password: str) -> str:
        result = await self.session.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        if user is None or not verify_password(password, user.hashed_password):
            raise ValueError("invalid email or password")
        return create_token(user.id)

    async def get_user(self, user_id: str) -> User | None:
        result = await self.session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()
