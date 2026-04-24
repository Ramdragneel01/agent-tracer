
"""API tests for agent-tracer trace ingestion and retrieval."""

from __future__ import annotations

from dataclasses import replace

from fastapi.testclient import TestClient
import pytest

from api import main as main_module
from api.main import app, rate_limiter, tracer

client = TestClient(app)


def _override_settings(monkeypatch, **changes):
    """Apply temporary runtime setting overrides for API security tests."""

    monkeypatch.setattr(main_module, "settings", replace(main_module.settings, **changes))


@pytest.fixture(autouse=True)
def reset_api_state(monkeypatch):
    """Reset shared in-memory API state between tests for determinism."""

    tracer.clear()
    rate_limiter.clear()
    _override_settings(monkeypatch, api_key="", rate_limit_per_minute=600)

    yield

    tracer.clear()
    rate_limiter.clear()


def test_health_endpoint_returns_ok() -> None:
    """Ensures health endpoint responds with service status."""
    response = client.get("/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["service"] == "agent-tracer"


def test_trace_ingestion_and_latest_retrieval() -> None:
    """Ensures trace steps can be ingested and fetched."""

    ingest = client.post(
        "/trace",
        json={
            "steps": [
                {
                    "node_name": "retrieve",
                    "input_state": {"query": "hello"},
                    "output_state": {"docs": ["d1"]},
                    "latency_ms": 3.5,
                    "token_usage": 21,
                    "status": "success",
                }
            ]
        },
    )

    assert ingest.status_code == 200
    assert ingest.json()["stored"] == 1

    latest = client.get("/trace/latest")
    assert latest.status_code == 200
    payload = latest.json()
    assert payload["count"] == 1
    assert payload["steps"][0]["node_name"] == "retrieve"


def test_clear_trace_endpoint() -> None:
    """Ensures trace store can be cleared via API."""
    client.post(
        "/trace",
        json={
            "steps": [
                {
                    "node_name": "plan",
                    "input_state": {},
                    "output_state": {},
                    "latency_ms": 1.2,
                    "token_usage": 5,
                    "status": "success",
                }
            ]
        },
    )

    clear = client.delete("/trace")
    assert clear.status_code == 200
    assert clear.json()["status"] == "cleared"

    latest = client.get("/trace/latest")
    assert latest.status_code == 200
    assert latest.json()["count"] == 0


def test_trace_requires_api_key_when_configured(monkeypatch) -> None:
    """Ensures protected trace endpoints require API key when configured."""

    _override_settings(monkeypatch, api_key="secret-key")

    unauthorized = client.post(
        "/trace",
        json={
            "steps": [
                {
                    "node_name": "retrieve",
                    "input_state": {"query": "hello"},
                    "output_state": {"docs": ["d1"]},
                    "latency_ms": 3.5,
                    "token_usage": 21,
                    "status": "success",
                }
            ]
        },
    )
    assert unauthorized.status_code == 401

    authorized = client.post(
        "/trace",
        headers={"X-API-Key": "secret-key"},
        json={
            "steps": [
                {
                    "node_name": "retrieve",
                    "input_state": {"query": "hello"},
                    "output_state": {"docs": ["d1"]},
                    "latency_ms": 3.5,
                    "token_usage": 21,
                    "status": "success",
                }
            ]
        },
    )
    assert authorized.status_code == 200


def test_health_is_public_when_api_key_enabled(monkeypatch) -> None:
    """Ensures health endpoint remains public for probes and uptime checks."""

    _override_settings(monkeypatch, api_key="secret-key")
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_trace_write_rate_limit_returns_429(monkeypatch) -> None:
    """Ensures write endpoints return 429 when per-minute limit is exceeded."""

    _override_settings(monkeypatch, rate_limit_per_minute=1)

    first = client.post(
        "/trace",
        json={
            "steps": [
                {
                    "node_name": "retrieve",
                    "input_state": {"query": "hello"},
                    "output_state": {"docs": ["d1"]},
                    "latency_ms": 3.5,
                    "token_usage": 21,
                    "status": "success",
                }
            ]
        },
    )
    assert first.status_code == 200

    second = client.post(
        "/trace",
        json={
            "steps": [
                {
                    "node_name": "plan",
                    "input_state": {"docs": ["d1"]},
                    "output_state": {"plan": "use d1"},
                    "latency_ms": 2.2,
                    "token_usage": 15,
                    "status": "success",
                }
            ]
        },
    )
    assert second.status_code == 429
