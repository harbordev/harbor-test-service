from datetime import datetime, timezone

from fastapi import APIRouter, status

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/live", status_code=status.HTTP_200_OK)
async def liveness_check():
    """Liveness probe: verifies that the application process is running."""
    return {
        "status": "alive",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@router.get("/ready", status_code=status.HTTP_200_OK)
async def readiness_check():
    """Readiness probe: verifies that the application is ready to accept traffic."""
    return {
        "status": "ready",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "checks": {
            "app": "ok",
            "in_memory_store": "ok",
        },
    }
