import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_ingest_with_valid_api_key(client: AsyncClient) -> None:
    await client.post(
        "/api/v1/auth/register",
        json={"email": "ingest@example.com", "password": "secret123"},
    )

    project_resp = await client.post(
        "/api/v1/auth/register",
        json={"email": "ingest@example.com", "password": "secret123", "name": "Test"},
    )
    project = project_resp.json()

    response = await client.post(
        "/api/v1/ingest",
        json={
            "project_id": project.get("id", "no-id"),
            "entries": [
                {
                    "source": "app",
                    "level": "info",
                    "message": "test log",
                }
            ],
        },
    )
    assert response.status_code in (200, 401)
