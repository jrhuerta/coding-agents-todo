"""Tests for Todo model."""

from sqlalchemy import select

from app.models import Todo
from app.database import get_session


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
