# Harbor Test Service (`harbor-test-service`)

A lightweight Python FastAPI backend service designed specifically to test, validate, and demonstrate the [Harbor Platform](https://github.com/shanelperera/harbor) deployment lifecycle, GitHub Actions orchestration, environment injection, and status callbacks.

---

## Features

- **FastAPI Core**: Async, clean REST APIs with Pydantic v2 schemas and request validation.
- **Harbor Integration Contract**:
  - Implements `.github/workflows/deploy.yml` with Harbor's 6 mandatory `workflow_dispatch` inputs.
  - Generates HMAC-SHA256 signatures (`X-Harbor-Signature`) for status callbacks (`Running`, `Succeeded`, `Failed`) back to Harbor's `/api/deployments/{id}/status`.
- **Health Probes**: Liveness (`/health/live`) and Readiness (`/health/ready`) endpoints.
- **Environment Ingestion Verification**: `/api/v1/info` and `/api/v1/env-check` return runtime diagnostics and Harbor deployment metadata (`HARBOR_PROJECT_ID`, `HARBOR_SERVICE_ID`, `HARBOR_DEPLOYMENT_ID`, `GIT_COMMIT_SHA`).
- **Comprehensive Test Suite**: Pytest + HTTPX async tests with 100% route coverage.
- **Secure Docker Container**: Multi-stage build running as non-root user `appuser` (UID 10001) with internal container health checks.

---

## Project Structure

```text
harbor-test-service/
├── .github/
│   └── workflows/
│       ├── ci.yml                 # CI: Ruff linter & Pytest on push/PR
│       └── deploy.yml             # Harbor deployment dispatch & status callback
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

## Harbor Dispatch & Callback Contract

### 1. `workflow_dispatch` Inputs
When Harbor deploys a service, it triggers `.github/workflows/deploy.yml` with:
- `environment`: Target environment name (`Development`, `Staging`, `Production`)
- `project`: Harbor project ID
- `service`: Harbor service ID
- `deployment_id`: Harbor internal deployment ID
- `version`: Branch, tag, or version string
- `commit_sha`: Git commit SHA (or blank)

### 2. Status Callbacks to Harbor
During workflow execution, the job reports status back to Harbor:
- **Endpoint**: `POST {HARBOR_API_BASE_URL}/api/deployments/{deployment_id}/status`
- **Header**: `X-Harbor-Signature: <hex_hmac_sha256>`
- **Payload**: `{"status": "Running" | "Succeeded" | "Failed", "failureReason": "..."}`

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
# Run pytest with coverage
pytest

# Run linter
ruff check .
ruff format --check .
```

### 3. Run Application Locally
```bash
uvicorn app.main:app --reload --port 8000
```
Visit http://localhost:8000/docs for the Swagger UI.

### 4. Run via Docker Compose
```bash
docker compose up --build
```
