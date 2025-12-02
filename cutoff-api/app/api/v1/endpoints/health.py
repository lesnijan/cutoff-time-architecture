"""
Health check endpoint.
GET /health - No authentication required.
"""

import time
from datetime import datetime

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.core.logging import get_logger
from app.models.responses import HealthResponse

router = APIRouter()
logger = get_logger(__name__)

# Application start time for uptime calculation
_start_time = time.time()


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    description="Check API health status. No authentication required.",
    tags=["Health"],
)
async def health_check() -> HealthResponse:
    """
    Health check endpoint.

    Returns overall health status and component checks.
    """
    settings = get_settings()

    # Check components
    checks = {
        "hana": "ok",  # TODO: Implement actual HANA health check
        "redis": "ok",  # TODO: Implement actual Redis health check
        "api": "ok",
    }

    # Determine overall status
    if all(status == "ok" for status in checks.values()):
        overall_status = "healthy"
    elif any(status == "down" for status in checks.values()):
        overall_status = "unhealthy"
    else:
        overall_status = "degraded"

    # Calculate uptime
    uptime_seconds = int(time.time() - _start_time)

    response = HealthResponse(
        status=overall_status,
        version=settings.version,
        timestamp=datetime.now(),
        checks=checks,
        uptime_seconds=uptime_seconds,
    )

    # Return 503 if unhealthy
    if overall_status == "unhealthy":
        return JSONResponse(
            status_code=503,
            content=response.model_dump(mode="json"),
        )

    logger.debug("health_check_performed", status=overall_status, uptime=uptime_seconds)

    return response
