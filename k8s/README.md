# Kubernetes Rollout

This directory provides a production-oriented baseline deployment for agent-tracer.

Use environment overlays for rollout:

1. `k8s/overlays/dev`
2. `k8s/overlays/stage`
3. `k8s/overlays/prod`

## Included Resources

1. Backend Deployment, Service, HPA, probes.
2. Frontend Deployment, Service, HPA, probes.
3. Ingress with TLS and host-based routing.
4. Namespace and backend runtime ConfigMap.
5. Secret example file for API key injection.

## Prerequisites

1. Kubernetes cluster with metrics-server installed (required for HPA).
2. Ingress controller (manifests use `nginx` ingress class).
3. TLS certificate secret (`agent-tracer-tls`) in namespace `agent-tracer`.
4. Published container images for backend and frontend.

## Configure Images

Update images in these files before rollout:

1. `backend-deployment.yaml`
2. `frontend-deployment.yaml`

Example image targets:

1. `ghcr.io/<your-org>/agent-tracer-backend:<tag>`
2. `ghcr.io/<your-org>/agent-tracer-frontend:<tag>`

When building the frontend image, set `VITE_API_BASE_URL` to your backend ingress URL.

```bash
docker build -t ghcr.io/<your-org>/agent-tracer-frontend:<tag> \
  -f frontend/Dockerfile --build-arg VITE_API_BASE_URL=https://agent-tracer-api.example.com .
```

## Configure Hosts

Update hostnames in:

1. `backend-configmap.yaml` (`AGENT_TRACER_ALLOWED_ORIGINS`, `AGENT_TRACER_ALLOWED_HOSTS`)
2. `ingress.yaml` (`rules[].host`, `spec.tls[].hosts`)

## Create Backend API Secret

Use `backend-secret.example.yaml` as a template and apply your real secret values.

The example secret file is intentionally not included in `kustomization.yaml`.

```bash
kubectl create namespace agent-tracer
kubectl -n agent-tracer create secret generic agent-tracer-backend-secret \
  --from-literal=AGENT_TRACER_API_KEY='<strong-secret>'
```

## Deploy

Apply one environment overlay:

```bash
kubectl apply -k k8s/overlays/dev
kubectl apply -k k8s/overlays/stage
kubectl apply -k k8s/overlays/prod
```

Or render manifests for review:

```bash
kubectl kustomize k8s/overlays/prod
```

```bash
kubectl apply -k k8s/overlays/prod
```

## Verify

```bash
kubectl -n agent-tracer get pods
kubectl -n agent-tracer get svc
kubectl -n agent-tracer get ingress
kubectl -n agent-tracer get hpa
kubectl -n agent-tracer rollout status deploy/agent-tracer-backend
kubectl -n agent-tracer rollout status deploy/agent-tracer-frontend
```

## Rollback

```bash
kubectl -n agent-tracer rollout undo deploy/agent-tracer-backend
kubectl -n agent-tracer rollout undo deploy/agent-tracer-frontend
```
