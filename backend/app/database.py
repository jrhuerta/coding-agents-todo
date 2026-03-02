"""SQLAlchemy engine and session factory."""

import os
from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo.db")

# SQLite needs check_same_thread=False for FastAPI
_connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    _connect_args["check_same_thread"] = False

engine = create_engine(
    DATABASE_URL,
    connect_args=_connect_args,
    echo=False,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_engine():
    """Return the SQLAlchemy engine."""
    return engine


def get_session_factory() -> sessionmaker[Session]:
    """Return the session factory."""
    return SessionLocal


@contextmanager
def get_session() -> Generator[Session, None, None]:
    """Context manager yielding a database session."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
