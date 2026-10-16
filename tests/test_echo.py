import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_echo_endpoint(async_client: AsyncClient):
    payload = {"message": "hello harbor", "count": 3}
    res = await async_client.post("/api/v1/echo?trace_id=xyz-123", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["body"] == payload
    assert data["query_params"]["trace_id"] == "xyz-123"
