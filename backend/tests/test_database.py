"""Tests for database module."""

from sqlalchemy import text
from app.database import get_engine, get_session_factory, get_session


def test_engine_creates_with_in_memory_sqlite() -> None:
    """Engine works with in-memory SQLite."""
    engine = get_engine()
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        assert result.scalar() == 1


def test_session_factory_produces_sessions() -> None:
    """Session factory produces working sessions."""
    factory = get_session_factory()
    with factory() as session:
        result = session.execute(text("SELECT 1"))
        assert result.scalar() == 1


def test_get_session_context_manager() -> None:
    """get_session yields a working session."""
    with get_session() as session:
        result = session.execute(text("SELECT 1"))
        assert result.scalar() == 1
