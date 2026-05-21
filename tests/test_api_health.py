from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint_returns_ok():
    """Expose a lightweight API sanity check without touching the database."""
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
