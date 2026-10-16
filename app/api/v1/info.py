import os
import sys
import time

from fastapi import APIRouter, Depends

from app.core.config import Settings, get_settings

router = APIRouter(prefix="/api/v1", tags=["Information & Diagnostics"])

# Record start time for uptime calculation
START_TIME = time.time()


@router.get("/info")
async def get_service_info(settings: Settings = Depends(get_settings)):
    """
    Returns application info, host runtime diagnostics, and Harbor deployment metadata.
    This endpoint allows verifying that Harbor successfully passed deployment parameters
    into the running container.
    """
    uptime_seconds = round(time.time() - START_TIME, 2)
    return {
        "app_name": settings.APP_NAME,
        "app_version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "uptime_seconds": uptime_seconds,
        "python_version": sys.version,
        "harbor": {
            "project_id": settings.HARBOR_PROJECT_ID,
            "service_id": settings.HARBOR_SERVICE_ID,
            "deployment_id": settings.HARBOR_DEPLOYMENT_ID,
            "environment": settings.HARBOR_ENVIRONMENT,
            "commit_sha": settings.GIT_COMMIT_SHA,
        },
    }


@router.get("/env-check")
async def get_env_check(settings: Settings = Depends(get_settings)):
    """
    Sanitized environment inspection to verify Harbor environment variable injection.
    Sensitive keys containing 'SECRET', 'TOKEN', 'KEY', 'PASS' are masked.
    """
    sanitized_env = {}
    sensitive_keys = ("SECRET", "TOKEN", "KEY", "PASSWORD", "AUTH")

    for key, value in os.environ.items():
        upper_key = key.upper()
        if any(term in upper_key for term in sensitive_keys):
            sanitized_env[key] = f"***masked({len(value)} chars)***"
        elif key.startswith(("HARBOR_", "APP_", "PYTHON", "ENVIRONMENT")):
            sanitized_env[key] = value

    return {
        "environment": settings.ENVIRONMENT,
        "harbor_configured": bool(settings.HARBOR_DEPLOYMENT_ID or settings.HARBOR_SERVICE_ID),
        "variables": sanitized_env,
    }
