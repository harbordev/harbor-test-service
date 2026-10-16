import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_items_crud_lifecycle(async_client: AsyncClient):
    # 1. Initial list should be empty
    res = await async_client.get("/api/v1/items")
    assert res.status_code == 200
    assert res.json() == []

    # 2. Create item
    payload = {"name": "Test Gadget", "description": "Harbor test asset", "price": 49.99}
    res = await async_client.post("/api/v1/items", json=payload)
    assert res.status_code == 201
    created = res.json()
    assert created["id"] == 1
    assert created["name"] == "Test Gadget"
    assert created["price"] == 49.99
    assert created["is_active"] is True

    # 3. Retrieve item
    res = await async_client.get(f"/api/v1/items/{created['id']}")
    assert res.status_code == 200
    assert res.json()["name"] == "Test Gadget"

    # 4. Update item
    update_payload = {"price": 39.99, "is_active": False}
    res = await async_client.put(f"/api/v1/items/{created['id']}", json=update_payload)
    assert res.status_code == 200
    updated = res.json()
    assert updated["price"] == 39.99
    assert updated["is_active"] is False

    # 5. Delete item
    res = await async_client.delete(f"/api/v1/items/{created['id']}")
    assert res.status_code == 204

    # 6. Verify 404
    res = await async_client.get(f"/api/v1/items/{created['id']}")
    assert res.status_code == 404


@pytest.mark.asyncio
async def test_create_item_validation(async_client: AsyncClient):
    bad_payload = {"name": "Invalid Item", "price": -5.0}
    res = await async_client.post("/api/v1/items", json=bad_payload)
    assert res.status_code == 422
