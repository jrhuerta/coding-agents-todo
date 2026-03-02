"""Pytest configuration and fixtures."""

import os

# Force in-memory SQLite for all tests before any app imports
os.environ["DATABASE_URL"] = "sqlite:///:memory:"
