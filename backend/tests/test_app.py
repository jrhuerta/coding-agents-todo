"""Tests for FastAPI app."""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_app_responds_to_root(client: TestClient) -> None:
    """App responds to GET /."""
    response = client.get("/")
    assert response.status_code == 200


def test_cors_allows_localhost_5173(client: TestClient) -> None:
    """CORS allows origin http://localhost:5173."""
    response = client.options(
        "/",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert response.status_code == 200
    assert "access-control-allow-origin" in [
        h.lower() for h in response.headers
    ]
    assert "http://localhost:5173" in response.headers.get(
        "access-control-allow-origin", ""
    )
