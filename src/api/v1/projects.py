from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import get_current_user, get_session
from models.postgres_models import Project, User
from repositories.project import ProjectRepository
from schemas.project import ProjectCreate, ProjectRead, ProjectUpdate

router = APIRouter(prefix="/projects", tags=["projects"])


def _project_to_read(project: Project) -> ProjectRead:
    return ProjectRead(
        id=project.id,
        owner_id=project.owner_id,
        name=project.name,
        description=project.description,
        api_key=project.api_key,
        created_at=project.created_at,
    )


@router.post("", response_model=ProjectRead, status_code=201)
async def create_project(
    data: ProjectCreate,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    repo = ProjectRepository(session)
    project = Project(
        owner_id=user.id,
        name=data.name,
        description=data.description,
    )
    project = await repo.save(project)
    return _project_to_read(project)


@router.get("", response_model=list[ProjectRead])
async def list_projects(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    repo = ProjectRepository(session)
    projects, _ = await repo.list(filters={"owner_id": user.id})
    return [_project_to_read(p) for p in projects]


@router.get("/{project_id}", response_model=ProjectRead)
async def get_project(
    project_id: str,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    repo = ProjectRepository(session)
    project = await repo.get(project_id)
    if project is None or project.owner_id != user.id:
        raise HTTPException(status_code=404, detail="project not found")
    return _project_to_read(project)


@router.put("/{project_id}", response_model=ProjectRead)
async def update_project(
    project_id: str,
    data: ProjectUpdate,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    repo = ProjectRepository(session)
    project = await repo.get(project_id)
    if project is None or project.owner_id != user.id:
        raise HTTPException(status_code=404, detail="project not found")
    if data.name is not None:
        project.name = data.name
    if data.description is not None:
        project.description = data.description
    project = await repo.save(project)
    return _project_to_read(project)


@router.delete("/{project_id}", status_code=204)
async def delete_project(
    project_id: str,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    repo = ProjectRepository(session)
    project = await repo.get(project_id)
    if project is None or project.owner_id != user.id:
        raise HTTPException(status_code=404, detail="project not found")
    await repo.delete(project_id)


@router.post("/{project_id}/regenerate-key", response_model=ProjectRead)
async def regenerate_key(
    project_id: str,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    repo = ProjectRepository(session)
    project = await repo.get(project_id)
    if project is None or project.owner_id != user.id:
        raise HTTPException(status_code=404, detail="project not found")
    new_key = await repo.regenerate_api_key(project_id)
    if new_key is None:
        raise HTTPException(status_code=404, detail="project not found")
    return _project_to_read(project)
