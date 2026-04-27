# Deployment Guide

## Prerequisites

1. Python 3.11+
2. Node.js 20+

## Backend Setup

```bash
pip install -r requirements-prod.txt
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
3. `AGENT_TRACER_MAX_STEPS` (default `10000`, bounded in-memory retention)
4. `AGENT_TRACER_ALLOWED_ORIGINS` (comma-separated CORS allow-list)
5. `AGENT_TRACER_ALLOWED_HOSTS` (comma-separated host header allow-list)
6. `AGENT_TRACER_ENABLE_DOCS` (`true`/`false`, API docs exposure)
7. `AGENT_TRACER_ENABLE_GZIP` (`true`/`false`, response compression)
8. `AGENT_TRACER_HSTS_SECONDS` (default `0`; set only when TLS terminates before app)
9. `AGENT_TRACER_LOG_LEVEL` (default `INFO`)
10. `VITE_API_BASE_URL` (frontend API base URL)

## Container Deployment

1. Create runtime env file:

```bash
cp .env.example .env
```

2. Set production-safe values in `.env` (minimum: API key, allowed hosts/origins, max retention).

3. Build and start services:

```bash
docker compose up --build -d
```

4. Validate probes:

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/ready
```

## Kubernetes Deployment

1. Build and publish immutable image tags for backend and frontend.
2. Update image references in `k8s/backend-deployment.yaml` and `k8s/frontend-deployment.yaml`.
3. Configure hostnames in `k8s/backend-configmap.yaml` and `k8s/ingress.yaml`.
4. Create namespace and backend API key secret:

```bash
kubectl create namespace agent-tracer
kubectl -n agent-tracer create secret generic agent-tracer-backend-secret \
	--from-literal=AGENT_TRACER_API_KEY='<strong-secret>'
```

5. Apply manifests:

```bash
kubectl apply -k k8s/overlays/dev
kubectl apply -k k8s/overlays/stage
kubectl apply -k k8s/overlays/prod
```

Use the command for the single target environment in your rollout stage.

Optional manifest preview:

```bash
kubectl kustomize k8s/overlays/prod
```

6. Verify rollout:

```bash
kubectl -n agent-tracer get pods,svc,ingress,hpa
kubectl -n agent-tracer rollout status deploy/agent-tracer-backend
kubectl -n agent-tracer rollout status deploy/agent-tracer-frontend
```

7. Roll back if needed:

```bash
kubectl -n agent-tracer rollout undo deploy/agent-tracer-backend
kubectl -n agent-tracer rollout undo deploy/agent-tracer-frontend
```

For full pre/post release controls, use `docs/PRODUCTION_CHECKLIST.md`.

## Runtime Security Notes

1. Keep `AGENT_TRACER_API_KEY` in a secret manager, not in source control.
2. Use HTTPS and reverse-proxy access controls in production.
3. Set explicit `AGENT_TRACER_ALLOWED_HOSTS` and `AGENT_TRACER_ALLOWED_ORIGINS` values.
4. Restrict trace payload content when handling sensitive state.

## CI and Release

1. CI workflow: `.github/workflows/ci.yml`
2. Release workflow: `.github/workflows/release.yml`
