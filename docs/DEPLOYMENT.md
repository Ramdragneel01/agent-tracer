# Deployment Guide

## Prerequisites

1. Python 3.11+
2. Node.js 20+

## Backend Setup

```bash
pip install -r requirements.txt
uvicorn api.main:app --host 0.0.0.0 --port 8000
```

## Frontend Build

```bash
cd frontend
npm ci
npm run build
```

## Environment Variables

1. `AGENT_TRACER_API_KEY` (optional, enables API key auth on protected endpoints)
2. `AGENT_TRACER_RATE_LIMIT_PER_MINUTE` (default `600`)
3. `VITE_API_BASE_URL` (frontend API base URL)

## Runtime Security Notes

1. Keep `AGENT_TRACER_API_KEY` in a secret manager, not in source control.
2. Use HTTPS and reverse-proxy access controls in production.
3. Restrict trace payload content when handling sensitive state.

## CI and Release

1. CI workflow: `.github/workflows/ci.yml`
2. Release workflow: `.github/workflows/release.yml`
