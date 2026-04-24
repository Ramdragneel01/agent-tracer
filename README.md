# agent-tracer

Observability toolkit for LangGraph-style multi-agent pipelines.

## Features

- One-line graph instrumentation via `AgentTracer.trace(graph)`.
- Per-node trace capture: input state, output state, latency, token usage, timestamp, and status.
- JSON trace export for storage or downstream analysis.
- Rich terminal renderer for timeline inspection.
- FastAPI endpoints for trace ingestion and retrieval.
- Minimal React timeline UI that auto-refreshes from `/trace/latest`.

## Project Layout

- `src/tracer.py`: core tracer + `TraceStep` dataclass.
- `src/renderer.py`: rich terminal timeline renderer.
- `api/main.py`: FastAPI app with `/trace` and `/trace/latest`.
- `examples/demo_graph.py`: runnable 3-node graph demo.
- `frontend/`: Vite + React timeline UI.
- `tests/`: pytest suite for tracer, API, and renderer.

## Quick Start

### Backend

```bash
pip install -r requirements.txt
uvicorn api.main:app --reload
```

Optional security env vars:

```bash
AGENT_TRACER_API_KEY=
AGENT_TRACER_RATE_LIMIT_PER_MINUTE=600
```

### Run Demo Graph

```bash
python examples/demo_graph.py
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Set API base URL if needed:

```bash
VITE_API_BASE_URL=http://127.0.0.1:8000
```

## API Endpoints

- `GET /health` - service health summary.
- `POST /trace` - ingest one or more trace steps (protected when API key is configured).
- `GET /trace/latest` - fetch latest trace timeline (protected when API key is configured).
- `DELETE /trace` - clear in-memory trace state (protected when API key is configured).

Write endpoints are rate-limited per client using in-memory throttling.

## Example Instrumentation

```python
from src.tracer import AgentTracer

tracer = AgentTracer()
traced_graph = tracer.trace(graph)
traced_graph.invoke({"query": "hello"})

print(tracer.export_json())
```

## Validation

```bash
pytest -q
```

Frontend build validation:

```bash
cd frontend
npm ci
npm run build
```

## Production Baseline

1. Architecture: `ARCHITECTURE.md`
2. Contribution guide: `CONTRIBUTING.md`
3. Security policy: `SECURITY.md`
4. Changelog: `CHANGELOG.md`
5. Collaboration context: `.claude/CLAUDE.md`
6. API docs: `docs/API.md`
7. Deployment docs: `docs/DEPLOYMENT.md`
8. Testing docs: `docs/TESTING.md`
9. CI workflow: `.github/workflows/ci.yml`
10. Release workflow: `.github/workflows/release.yml`

## Evidence

1. Backend tests validate ingestion/retrieval contracts and auth/rate-limit controls.
2. Frontend production build validates UI packaging integrity.
3. CI runs backend tests, frontend build, and dependency audit checks.

## Screenshot Placeholder

Add terminal timeline screenshot and frontend timeline screenshot here.

## Limitations

1. Trace storage is in-memory and resets on process restart.
2. Built-in rate limiting is per-instance and not distributed across replicas.
3. API key auth is shared-secret based and not role-aware.

## Next Roadmap

1. Add persistent trace storage backend with retention policies.
2. Add optional role-based auth integration for multi-tenant access.
3. Add advanced query filters and pagination for large trace timelines.
