import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_user(client: AsyncClient) -> None:
    response = await client.post(
        "/api/v1/auth/register",
        json={"email": "test@example.com", "password": "secret123", "name": "Test"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"


@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient) -> None:
    await client.post(
        "/api/v1/auth/register",
        json={"email": "dup@example.com", "password": "secret123"},
    )
    response = await client.post(
        "/api/v1/auth/register",
        json={"email": "dup@example.com", "password": "secret123"},
    )
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient) -> None:
    await client.post(
        "/api/v1/auth/register",
        json={"email": "login@example.com", "password": "secret123"},
    )
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": "login@example.com", "password": "secret123"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient) -> None:
    await client.post(
        "/api/v1/auth/register",
        json={"email": "wrong@example.com", "password": "secret123"},
    )
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": "wrong@example.com", "password": "wrongpass"},
    )
    assert response.status_code == 401
