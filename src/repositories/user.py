from models.postgres_models import User
from sqlalchemy import select

from repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    @property
    def model(self) -> type[User]:
        return User

    async def get_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
