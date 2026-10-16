import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_root_endpoint(async_client: AsyncClient):
    response = await async_client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "Harbor test service is online" in data["message"]


@pytest.mark.asyncio
async def test_info_endpoint(async_client: AsyncClient):
    response = await async_client.get("/api/v1/info")
    assert response.status_code == 200
    data = response.json()
    assert data["environment"] == "testing"
    assert data["harbor"]["project_id"] == "proj-test-123"
    assert data["harbor"]["service_id"] == "srv-test-456"
    assert data["harbor"]["deployment_id"] == "99"
    assert data["harbor"]["commit_sha"] == "a1b2c3d4e5f6"


@pytest.mark.asyncio
async def test_env_check_masking(async_client: AsyncClient):
    response = await async_client.get("/api/v1/env-check")
    assert response.status_code == 200
    data = response.json()
    assert data["harbor_configured"] is True
    variables = data["variables"]
    if "TEST_SECRET_KEY" in variables:
        assert "***masked" in variables["TEST_SECRET_KEY"]
