# Testing Guide

## Backend Tests

Run API and tracer unit tests:

```bash
pytest -q
```

Coverage includes:

1. Trace instrumentation behavior.
2. Renderer output.
3. API ingest, retrieval, and clear flows.
4. API key enforcement on protected endpoints.
5. Write-route rate-limit enforcement.

## Frontend Validation

Build frontend artifacts:

```bash
cd frontend
npm run build
```

## CI Gate

The CI workflow runs backend tests, frontend build, and dependency audits.
