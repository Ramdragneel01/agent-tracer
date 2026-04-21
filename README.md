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
- `POST /trace` - ingest one or more trace steps.
- `GET /trace/latest` - fetch latest trace timeline.
- `DELETE /trace` - clear in-memory trace state.

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

## Screenshot Placeholder

Add terminal timeline screenshot and frontend timeline screenshot here.
