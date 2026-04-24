# API Reference

Base URL defaults to `http://127.0.0.1:8000`.

## Authentication

Protected endpoints require `X-API-Key` only when `AGENT_TRACER_API_KEY` is configured.

## Endpoints

### `GET /health`

Public endpoint returning service health summary.

Response:

```json
{
  "status": "ok",
  "service": "agent-tracer",
  "trace_steps": 0
}
```

### `POST /trace`

Protected endpoint to ingest one or more trace steps.

Request:

```json
{
  "steps": [
    {
      "node_name": "retrieve",
      "input_state": {"query": "hello"},
      "output_state": {"docs": ["d1"]},
      "latency_ms": 3.5,
      "token_usage": 21,
      "status": "success"
    }
  ]
}
```

Response:

```json
{
  "stored": 1,
  "total_steps": 1
}
```

Possible errors:

1. `401 Unauthorized` when API key is configured and missing/invalid.
2. `429 Too Many Requests` when write limit is exceeded.
3. `422 Unprocessable Entity` for validation errors.

### `GET /trace/latest`

Protected endpoint returning latest trace steps.

Query parameters:

1. `limit` (optional, integer, default `200`, range `1..2000`)

Response:

```json
{
  "count": 1,
  "steps": [
    {
      "node_name": "retrieve",
      "input_state": {"query": "hello"},
      "output_state": {"docs": ["d1"]},
      "latency_ms": 3.5,
      "token_usage": 21,
      "timestamp": "2026-04-24T12:00:00+00:00",
      "status": "success",
      "error": null
    }
  ]
}
```

### `DELETE /trace`

Protected endpoint that clears in-memory trace state.

Response:

```json
{
  "status": "cleared"
}
```

Possible errors:

1. `401 Unauthorized` when API key is configured and missing/invalid.
2. `429 Too Many Requests` when write limit is exceeded.
