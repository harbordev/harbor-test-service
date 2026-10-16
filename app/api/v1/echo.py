from typing import Any, Dict

from fastapi import APIRouter, Request

router = APIRouter(prefix="/api/v1/echo", tags=["Diagnostics & Echo"])


@router.post("")
async def echo_request(request: Request, body: Dict[str, Any] | None = None):
    """Echoes back request headers, query parameters, and JSON payload."""
    return {
        "method": request.method,
        "url": str(request.url),
        "headers": dict(request.headers),
        "query_params": dict(request.query_params),
        "body": body or {},
    }
