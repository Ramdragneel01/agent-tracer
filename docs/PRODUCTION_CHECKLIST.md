# Production Checklist

Use this checklist before and after each production rollout.

## Release Metadata

1. Release tag is created and matches immutable image tags.
2. Commit SHA is recorded in release notes.
3. Change window and on-call owners are confirmed.

## Pre-Deploy Controls

1. CI is green (tests, dependency checks, container smoke builds).
2. Backend and frontend images are built and pushed.
3. Image tags in deployment manifests are pinned (no `latest`).
4. `AGENT_TRACER_ALLOWED_HOSTS` and `AGENT_TRACER_ALLOWED_ORIGINS` are set to production domains.
5. `AGENT_TRACER_ENABLE_DOCS=false` in production.
6. Ingress TLS secret (`agent-tracer-tls`) exists and certificate validity is checked.

## Secret Management

1. `AGENT_TRACER_API_KEY` is stored in Kubernetes Secret or external secret manager.
2. API key is never committed to source control.
3. Secret access is restricted to deployment namespace and runtime identity.
4. Secret rotation procedure is tested in non-production.

## Capacity and Resilience

1. Backend HPA and frontend HPA are active (`kubectl get hpa`).
2. Requests/limits are defined for all containers.
3. Readiness and liveness probes are passing for all pods.
4. Rollout strategy uses zero-downtime settings (`maxUnavailable: 0`).

## Backup and Restore

1. Current manifests and image tags are exported before deploy.
2. Last known-good deployment revisions are available for rollback.
3. Note: trace data is in-memory only; no persistent trace backup currently exists.
4. If persistent trace storage is introduced, backup frequency and restore drills must be added.

## Deployment Execution

1. Apply namespace/secret prerequisites.
2. Apply manifests with `kubectl apply -k k8s/`.
3. Wait for rollout completion for backend and frontend.
4. Validate ingress endpoints and API probes (`/health`, `/ready`).
5. Validate authenticated endpoint behavior (`/trace`, `/trace/latest`).

## Post-Deploy Validation

1. Error rate and latency are within baseline.
2. HPA target utilization is within expected range.
3. Synthetic smoke checks pass for frontend timeline view and API endpoints.
4. No unexpected restarts (`kubectl get pods` restart counts stable).

## Rollback Runbook

1. Trigger rollback if SLO violation persists beyond 10 minutes.
2. Roll back backend: `kubectl -n agent-tracer rollout undo deploy/agent-tracer-backend`.
3. Roll back frontend: `kubectl -n agent-tracer rollout undo deploy/agent-tracer-frontend`.
4. Confirm previous revisions are healthy and probe-ready.
5. Document incident timeline, root cause, and follow-up actions.

## Secret Rotation Defaults

1. Rotate `AGENT_TRACER_API_KEY` every 90 days.
2. Immediate rotation is required after suspected leak or role change.
3. Rotation process: create new secret value in manager, update Kubernetes secret, roll backend deployment, and revoke old key after validation.

## SLO and Alert Defaults

### SLOs

1. API availability (`/health` and `/ready` success): 99.9% per 30 days.
2. `GET /trace/latest` p95 latency: < 300 ms.
3. `POST /trace` p95 latency: < 500 ms.
4. 5xx error ratio: < 1% per 5-minute window.

### Alerts

1. Critical: API availability < 99.0% over 10 minutes.
2. Critical: 5xx ratio > 5% over 5 minutes.
3. Warning: p95 `GET /trace/latest` latency > 500 ms for 15 minutes.
4. Warning: backend HPA maxed out for 15 minutes.
5. Warning: pod restart count increases continuously for 10 minutes.
