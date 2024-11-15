import pytest
from httpx import AsyncClient

from app.users.schema import CreateUserRequestSchema


@pytest.mark.asyncio
async def test_create_user(client: AsyncClient):
    new_user = CreateUserRequestSchema(
        email="tes1t@example.com",
        password="password123",
        first_name="Test",
        last_name="User",
        gender="Other"
    )
    data = new_user.model_dump()
    
    response = await client.post("/api/user/", json=data)
    assert response.status_code == 201
    assert response.json()["email"] == new_user.email


@pytest.mark.asyncio
async def test_get_users_no_params(client: AsyncClient):
    new_user = CreateUserRequestSchema(
        email="test@example.com",
        password="password123",
        first_name="Test1",
        last_name="User",
        gender="Other"
    )
    data = new_user.model_dump()
    
    response = await client.post("/api/user/", json=data)

    response = await client.get("/api/user/all")

    assert response.status_code == 200
    assert len(response.json()) == 2


@pytest.mark.asyncio
async def test_get_users_with_search(client: AsyncClient):

    response = await client.get("/api/user/all?search=Test1")

    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_get_users_with_is_active(client: AsyncClient):
    response = await client.get("/api/user/all?is_active=true")

    assert response.status_code == 200
    assert len(response.json()) == 2


@pytest.mark.asyncio
async def test_get_user_success(client: AsyncClient, token):
    user_id = 2
    response = await client.get(f"/api/user/{user_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_update_user(client: AsyncClient, token):
    user_id = 2
    response = await client.put(f"/api/user/{user_id}", json={"first_name": "Test"},
                                headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["first_name"] == "Test"


@pytest.mark.asyncio
async def test_delete_user_not_authorized(client: AsyncClient, token):
    user_id = 4
    response = await client.delete(f"/api/user/{user_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_delete_user(client: AsyncClient, token):
    user_id = 2
    response = await client.delete(f"/api/user/{user_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 204


