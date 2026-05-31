from uuid import uuid4

from sqlalchemy import select

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
        project = await self.get(project_id)
        if project is None:
            return None
        project.api_key = uuid4().hex
        await self.session.flush()
        await self.session.refresh(project)
        return project.api_key
