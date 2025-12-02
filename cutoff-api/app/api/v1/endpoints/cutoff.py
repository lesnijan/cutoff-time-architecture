"""
Cutoff time endpoint.
GET /cutoff/current - Get current dynamic cutoff time.
"""

from datetime import datetime, timedelta
from decimal import Decimal

from fastapi import APIRouter, HTTPException, Query

from app.core.logging import get_logger
from app.models.domain import AlertLevel, DecisionStatus
from app.models.responses import CutoffStatusResponse, StatusHistoryPoint
from app.repositories.hana_repository import get_hana_repository

router = APIRouter()
logger = get_logger(__name__)


@router.get(
    "/cutoff/current",
    response_model=CutoffStatusResponse,
    summary="Get current cutoff time",
    description="Get the current dynamic cutoff time and warehouse status.",
    tags=["Cutoff"],
)
async def get_current_cutoff(
    warehouse_id: str = Query(default="WH-MAIN", description="Warehouse identifier"),
    # Uncomment for auth: user: User = Depends(require_read_scope)
) -> CutoffStatusResponse:
    """
    Get current cutoff time and warehouse status.

    This endpoint:
    1. Queries current warehouse state from HANA
    2. Calculates dynamic cutoff time
    3. Returns status and trend information
    """
    hana_repo = get_hana_repository()

    try:
        cutoff_data = await hana_repo.get_cutoff_calculation(warehouse_id)
    except Exception as e:
        logger.error("cutoff_query_failed", warehouse_id=warehouse_id, error=str(e))
        raise HTTPException(
            status_code=503,
            detail="Failed to query cutoff calculation from database",
        )

    # Extract data
    current_utilization = cutoff_data["current_utilization"]
    system_status = cutoff_data["system_status"]
    capacity = cutoff_data["current_capacity"]
    workload = cutoff_data["total_remaining_workload"]

    # Calculate cutoff time
    now = datetime.now()
    hard_deadline = now.replace(hour=16, minute=0, second=0, microsecond=0)
    if now >= hard_deadline:
        hard_deadline += timedelta(days=1)

    # Calculate processing time
    processing_time_minutes = float(workload / capacity) if capacity > 0 else 0
    safety_buffer_minutes = 30

    cutoff_time = hard_deadline - timedelta(minutes=processing_time_minutes + safety_buffer_minutes)

    # Calculate remaining time
    time_remaining_minutes = int((cutoff_time - now).total_seconds() / 60)
    if time_remaining_minutes < 0:
        time_remaining_minutes = 0
        system_status = DecisionStatus.CLOSED

    # Estimate orders in queue and remaining
    # TODO: Get actual values from HANA
    orders_in_queue = 47
    estimated_orders_remaining = max(0, int((1 - float(current_utilization)) * 100))

    # Determine trend (placeholder - would need historical data)
    trend = "STABLE"
    if current_utilization > Decimal("0.80"):
        trend = "INCREASING"
    elif current_utilization < Decimal("0.60"):
        trend = "DECREASING"

    # Determine alert level
    if system_status == DecisionStatus.CLOSED:
        alert_level = AlertLevel.CRITICAL
    elif system_status == DecisionStatus.CRITICAL:
        alert_level = AlertLevel.CRITICAL
    elif system_status == DecisionStatus.WARNING:
        alert_level = AlertLevel.WARNING
    else:
        alert_level = AlertLevel.NONE

    # Mock status history (TODO: Get from cache/database)
    status_history = [
        StatusHistoryPoint(
            time="11:00",
            status=DecisionStatus.ACCEPTING,
            utilization=Decimal("0.65"),
        ),
        StatusHistoryPoint(
            time="11:30",
            status=DecisionStatus.ACCEPTING,
            utilization=Decimal("0.71"),
        ),
        StatusHistoryPoint(
            time="12:00",
            status=system_status,
            utilization=current_utilization,
        ),
    ]

    logger.info(
        "cutoff_retrieved",
        warehouse_id=warehouse_id,
        cutoff_time=cutoff_time.isoformat(),
        status=system_status.value,
        utilization=float(current_utilization),
    )

    return CutoffStatusResponse(
        cutoff_time=cutoff_time,
        hard_deadline=hard_deadline,
        current_time=now,
        time_remaining_minutes=time_remaining_minutes,
        current_utilization=current_utilization,
        orders_in_queue=orders_in_queue,
        estimated_orders_remaining=estimated_orders_remaining,
        status=system_status,
        trend=trend,
        alert_level=alert_level,
        status_history=status_history,
    )
