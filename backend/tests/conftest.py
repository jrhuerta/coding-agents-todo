"""Pytest configuration and fixtures."""

import os

import pytest

# Force in-memory SQLite for all tests before any app imports
os.environ["DATABASE_URL"] = "sqlite:///:memory:"


@pytest.fixture(scope="session", autouse=True)
def _create_tables() -> None:
    """Create database tables from models before any test runs."""
    from app.models import Base
    from app.database import get_engine

    Base.metadata.create_all(get_engine())
