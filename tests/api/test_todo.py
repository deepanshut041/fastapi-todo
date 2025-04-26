import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


# Create
@pytest.mark.asyncio
async def test_create_todo(client: AsyncClient):
    payload = {"content": "Test todo"}
    response = await client.post("api/v1/todos", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["content"] == "Test todo"

# Retrieve
@pytest.mark.asyncio
async def test_retrieve_todo(client: AsyncClient):
    payload = {"content": "Test retrieve"}
    create_response = await client.post("/api/v1/todos", json=payload)
    todo_id = create_response.json()["id"]

    get_response = await client.get(f"/api/v1/todos/{todo_id}")
    assert get_response.status_code == 200
    data = get_response.json()
    assert data["content"] == "Test retrieve"

# # List
@pytest.mark.asyncio
async def test_list_todos(client: AsyncClient):
    await client.post("/api/v1/todos", json={"content": "List me 1"})
    await client.post("/api/v1/todos", json={"content": "List me 2"})

    response = await client.get("/api/v1/todos")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] >= 2
    assert any(item["content"] == "List me 1" for item in data["items"])

# Update
@pytest.mark.asyncio
async def test_update_todo(client: AsyncClient):
    create_resp = await client.post("/api/v1/todos", json={"content": "Old content"})
    todo_id = create_resp.json()["id"]

    update_resp = await client.put(f"/api/v1/todos/{todo_id}", json={"content": "New content"})
    assert update_resp.status_code == 200
    assert update_resp.json()["content"] == "New content"

# Delete
@pytest.mark.asyncio
async def test_delete_todo(client: AsyncClient):
    create_resp = await client.post("/api/v1/todos", json={"content": "To delete"})
    todo_id = create_resp.json()["id"]

    delete_resp = await client.delete(f"/api/v1/todos/{todo_id}")
    assert delete_resp.status_code == 204

    get_resp = await client.get(f"/api/v1/todos/{todo_id}")
    assert get_resp.status_code == 404
