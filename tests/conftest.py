import os

import pytest
from httpx import ASGITransport, AsyncClient

# Enforce testing environment variables
os.environ["ENVIRONMENT"] = "testing"
os.environ["HARBOR_PROJECT_ID"] = "proj-test-123"
os.environ["HARBOR_SERVICE_ID"] = "srv-test-456"
os.environ["HARBOR_DEPLOYMENT_ID"] = "99"
os.environ["HARBOR_ENVIRONMENT"] = "test-env"
os.environ["GIT_COMMIT_SHA"] = "a1b2c3d4e5f6"
os.environ["TEST_SECRET_KEY"] = "super-secret-value"

from app.api.v1.items import reset_store
from app.core.config import get_settings
from app.main import app


@pytest.fixture(autouse=True)
def clean_store():
    """Reset the in-memory item store and cache between tests."""
    reset_store()
    get_settings.cache_clear()
    yield
    reset_store()
    get_settings.cache_clear()


@pytest.fixture
async def async_client():
    """Async HTTP client targeting the ASGI FastAPI app."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        yield client
