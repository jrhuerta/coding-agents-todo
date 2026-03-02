"""Tests for Todo model."""

import pytest
from sqlalchemy import select

from app.models import Base, Todo
from app.database import get_engine, get_session


@pytest.fixture(scope="session", autouse=True)
def _create_tables() -> None:
    """Create database tables from models before any test runs."""
    Base.metadata.create_all(get_engine())


def test_can_import_todo_from_app_models() -> None:
    """Todo can be imported from app.models."""
    assert Todo is not None


def test_todo_has_expected_columns() -> None:
    """Todo model has id, title, completed, created_at columns."""
    todo = Todo(title="Test task")
    assert hasattr(todo, "id")
    assert hasattr(todo, "title")
    assert hasattr(todo, "completed")
    assert hasattr(todo, "created_at")


def test_todo_default_values() -> None:
    """Todo has correct defaults: completed=False, created_at set."""
    todo = Todo(title="Buy milk")
    assert todo.title == "Buy milk"
    with get_session() as session:
        session.add(todo)
        session.flush()
        assert todo.completed is False
        assert todo.created_at is not None


def test_todo_persistence() -> None:
    """Todo can be created and persisted to the database."""
    with get_session() as session:
        todo = Todo(title="Persist me", completed=False)
        session.add(todo)
        session.flush()
        todo_id = todo.id
        assert todo_id is not None

    with get_session() as session:
        result = session.execute(select(Todo).where(Todo.id == todo_id))
        loaded = result.scalar_one()
        assert loaded.title == "Persist me"
        assert loaded.completed is False
        assert loaded.created_at is not None
