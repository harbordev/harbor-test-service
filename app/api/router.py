from fastapi import APIRouter

from app.api.v1.echo import router as echo_router
from app.api.v1.health import router as health_router
from app.api.v1.info import router as info_router
from app.api.v1.items import router as items_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(info_router)
api_router.include_router(items_router)
api_router.include_router(echo_router)
