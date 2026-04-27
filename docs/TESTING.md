# Testing Guide

## Backend Tests

Run API and tracer unit tests:

```bash
pytest -q
```

Coverage includes:

1. Trace instrumentation behavior.
2. Renderer output.
3. API ingest, retrieval, readiness, and clear flows.
4. API key enforcement on protected endpoints.
5. Write-route rate-limit enforcement.
6. Response request-id and baseline security headers.

## Frontend Validation

Build frontend artifacts:

```bash
cd frontend
npm run build
```

## Container Build Validation

Build production images:

```bash
docker compose build
```

## CI Gate

The CI workflow runs backend tests, frontend build, and dependency audits.
