# Contributing

Thanks for contributing to agent-tracer.

## Setup

1. Use Python 3.11+.
2. Install backend dependencies:

```bash
pip install -r requirements.txt
```

3. Install frontend dependencies:

```bash
cd frontend
npm ci
```

## Quality Gates

Run before opening a pull request:

1. Backend tests:

```bash
pytest -q
```

2. Frontend production build:

```bash
cd frontend
npm run build
```

## Pull Request Guidance

1. Keep each PR focused on one behavior area.
2. Add or update tests for API behavior changes.
3. Update docs when endpoint contracts or env vars change.
4. Never commit secrets or credentials.
