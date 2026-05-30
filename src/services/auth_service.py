import logging

from core.security import create_token, hash_password, verify_password
from models.postgres_models import Project, User
from schemas.user import UserCreate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class AuthService:
    def __init__(self, session: AsyncSession) -> None:
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
        logger.info("user registered: %s", user.email)
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

    async def create_project(
        self, user_id: str, name: str, description: str | None = None
    ) -> Project:
        project = Project(owner_id=user_id, name=name, description=description)
        self.session.add(project)
        await self.session.flush()
        await self.session.refresh(project)
        return project
