from datetime import datetime, timezone
from typing import Dict, List

from fastapi import APIRouter, HTTPException, status

from app.models.item import ItemCreate, ItemResponse, ItemUpdate

router = APIRouter(prefix="/api/v1/items", tags=["Items CRUD"])

# In-memory data store for testing
_items_store: Dict[int, dict] = {}
_id_counter: int = 0


def reset_store():
    """Helper for testing to reset state."""
    global _items_store, _id_counter
    _items_store = {}
    _id_counter = 0


@router.get("", response_model=List[ItemResponse])
async def list_items():
    """List all stored items."""
    return list(_items_store.values())


@router.post("", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(item_in: ItemCreate):
    """Create a new item."""
    global _id_counter
    _id_counter += 1
    new_item = {
        "id": _id_counter,
        "name": item_in.name,
        "description": item_in.description,
        "price": item_in.price,
        "is_active": item_in.is_active,
        "created_at": datetime.now(timezone.utc),
    }
    _items_store[_id_counter] = new_item
    return new_item


@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int):
    """Retrieve an item by ID."""
    if item_id not in _items_store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found",
        )
    return _items_store[item_id]


@router.put("/{item_id}", response_model=ItemResponse)
async def update_item(item_id: int, item_in: ItemUpdate):
    """Update an existing item."""
    if item_id not in _items_store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found",
        )
    existing = _items_store[item_id]
    update_data = item_in.model_dump(exclude_unset=True)
    existing.update(update_data)
    return existing


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int):
    """Delete an item by ID."""
    if item_id not in _items_store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found",
        )
    del _items_store[item_id]
    return None
