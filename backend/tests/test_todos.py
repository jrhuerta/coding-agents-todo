"""Tests for todos API endpoints."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import delete

from app.database import get_session
from app.main import app
from app.models import Todo


@pytest.fixture(autouse=True)
def _clear_todos() -> None:
    """Clear todos table before each test for isolation."""
    with get_session() as session:
        session.execute(delete(Todo))


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_list_todos_empty(client: TestClient) -> None:
    """GET /todos returns empty list when no todos exist."""
    response = client.get("/todos")
    assert response.status_code == 200
    assert response.json() == []


def test_create_todo(client: TestClient) -> None:
    """POST /todos creates a todo and returns it."""
    response = client.post("/todos", json={"title": "Buy milk"})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Buy milk"
    assert data["completed"] is False
    assert "id" in data
    assert "created_at" in data


def test_list_todos_returns_created(client: TestClient) -> None:
    """GET /todos returns created todos."""
    client.post("/todos", json={"title": "Task one"})
    client.post("/todos", json={"title": "Task two"})
    response = client.get("/todos")
    assert response.status_code == 200
    items = response.json()
    assert len(items) == 2
    titles = [t["title"] for t in items]
    assert "Task one" in titles
    assert "Task two" in titles


def test_patch_todo(client: TestClient) -> None:
    """PATCH /todos/{id} updates a todo."""
    create_resp = client.post("/todos", json={"title": "Original"})
    todo_id = create_resp.json()["id"]

    response = client.patch(f"/todos/{todo_id}", json={"title": "Updated"})
    assert response.status_code == 200
    assert response.json()["title"] == "Updated"

    response = client.patch(f"/todos/{todo_id}", json={"completed": True})
    assert response.status_code == 200
    assert response.json()["completed"] is True


def test_delete_todo(client: TestClient) -> None:
    """DELETE /todos/{id} removes a todo."""
    create_resp = client.post("/todos", json={"title": "To delete"})
    todo_id = create_resp.json()["id"]

    response = client.delete(f"/todos/{todo_id}")
    assert response.status_code == 204

    response = client.get("/todos")
    assert len(response.json()) == 0


def test_patch_nonexistent_returns_404(client: TestClient) -> None:
    """PATCH /todos/{id} returns 404 for non-existent id."""
    response = client.patch("/todos/99999", json={"title": "Nope"})
    assert response.status_code == 404


def test_delete_nonexistent_returns_404(client: TestClient) -> None:
    """DELETE /todos/{id} returns 404 for non-existent id."""
    response = client.delete("/todos/99999")
    assert response.status_code == 404
