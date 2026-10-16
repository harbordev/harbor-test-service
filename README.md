# Harbor Test Service (`harbor-test-service`)

A lightweight Python FastAPI backend service designed specifically to test and demonstrate the [Harbor Platform](https://github.com/shanelperera/harbor) deployment lifecycle, GitHub Actions orchestration, environment injection, and health monitoring.

---

## Features

- **FastAPI Core**: Async REST API with Pydantic v2 schemas and request validation.
- **Harbor Native Integration**:
  - Implements `.github/workflows/deploy.yml` with Harbor's 6 mandatory `workflow_dispatch` inputs.
  - Zero secrets or curl callbacks needed in repository settings — Harbor tracks deployment progress automatically via GitHub App `workflow_run` webhooks.
- **Health Probes**: Liveness (`/health/live`) and Readiness (`/health/ready`) endpoints.
- **Environment Ingestion Verification**: `/api/v1/info` and `/api/v1/env-check` return runtime diagnostics and Harbor deployment metadata (`HARBOR_PROJECT_ID`, `HARBOR_SERVICE_ID`, `HARBOR_DEPLOYMENT_ID`, `GIT_COMMIT_SHA`).
- **Test Suite**: Pytest + HTTPX async tests with 98% route coverage.
- **Secure Docker Container**: Multi-stage build running as non-root user `appuser` (UID 10001) with internal container health checks.

---

## Project Structure

```text
harbor-test-service/
├── .github/
│   └── workflows/
│       ├── ci.yml                 # CI: Ruff linter & Pytest on push/PR
│       └── deploy.yml             # Harbor deployment dispatch workflow
├── app/
│   ├── main.py                    # FastAPI entrypoint, lifespan, and CORS setup
│   ├── core/
│   │   └── config.py              # Pydantic BaseSettings (Harbor metadata & env vars)
│   ├── api/
│   │   ├── router.py              # Aggregated API router
│   │   └── v1/
│   │       ├── health.py          # Liveness & readiness probes (/health/live, /health/ready)
│   │       ├── info.py            # Deployment info & environment verification
│   │       ├── items.py           # Sample CRUD resource API
│   │       └── echo.py            # Diagnostic echo endpoint
│   └── models/
│       └── item.py                # Pydantic data schemas
├── tests/
│   ├── conftest.py                # Async HTTP test fixtures (httpx.AsyncClient)
│   ├── test_health.py             # Health check tests
│   ├── test_info.py               # Metadata & Harbor env var tests
│   ├── test_items.py              # CRUD API tests
│   └── test_echo.py               # Echo endpoint tests
├── scripts/
│   ├── test.sh                    # Test execution script
│   └── deploy.sh                  # Local deployment simulation script
├── Dockerfile                     # Multi-stage, unprivileged non-root image
├── .dockerignore                  # Build context exclusion
├── docker-compose.yml             # Local container run & health verification
├── pyproject.toml                 # Ruff, Pytest, and project metadata
├── requirements.txt               # App dependencies
├── requirements-dev.txt           # Test/Lint dependencies
└── .env.example                   # Local environment variable template
```

---

## Harbor Dispatch Contract

When Harbor deploys this service, it triggers `.github/workflows/deploy.yml` with:
- `environment`: Target environment name (`Development`, `Staging`, `Production`)
- `project`: Harbor project ID
- `service`: Harbor service ID
- `deployment_id`: Harbor internal deployment ID
- `version`: Branch, tag, or version string
- `commit_sha`: Git commit SHA (optional)

Harbor's GitHub App listens for the workflow run completion and automatically updates the deployment state in the Harbor UI and event stream.

---

## Local Development & Testing

### 1. Set Up Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
```

### 2. Run Tests & Linter
```bash
pytest
ruff check .
ruff format --check .
```

### 3. Run Application Locally
```bash
uvicorn app.main:app --reload --port 8000
```

### 4. Run via Docker Compose
```bash
docker compose up --build
```
