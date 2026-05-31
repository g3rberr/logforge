from uuid import uuid4

from sqlalchemy import select, update

from models.postgres_models import Project
from repositories.base import BaseRepository


class ProjectRepository(BaseRepository[Project]):
    @property
    def model(self) -> type[Project]:
        return Project

    async def get_by_api_key(self, api_key: str) -> Project | None:
        stmt = select(Project).where(Project.api_key == api_key)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def regenerate_api_key(self, project_id: str) -> str | None:
        new_key = uuid4().hex
        stmt = update(Project).where(Project.id == project_id).values(api_key=new_key)
        result = await self.session.execute(stmt)
        if result.rowcount == 0:  # type: ignore[attr-defined]
            return None
        await self.session.flush()
        return new_key
