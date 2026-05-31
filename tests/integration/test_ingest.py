import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from models.postgres_models import Project


@pytest.mark.asyncio
async def test_ingest_with_valid_api_key(client: AsyncClient, db_session: AsyncSession) -> None:
    user_resp = await client.post(
        "/api/v1/auth/register",
        json={"email": "ingest@example.com", "password": "secret123"},
    )
    user = user_resp.json()
    user_id = user["id"]

    project = Project(owner_id=user_id, name="Test Project", api_key="test-api-key-123")
    db_session.add(project)
    await db_session.commit()
    await db_session.refresh(project)

    response = await client.post(
        "/api/v1/ingest",
        json={"message": "test log", "source": "app", "level": "info"},
        headers={"X-API-Key": "test-api-key-123"},
    )
    assert response.status_code in (200, 201)
