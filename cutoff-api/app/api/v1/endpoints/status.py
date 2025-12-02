"""
Warehouse status endpoint.
GET /status - Comprehensive dashboard data.
"""

from datetime import datetime
from decimal import Decimal

from fastapi import APIRouter

from app.core.logging import get_logger
from app.models.domain import AlertLevel, DecisionStatus, ResourceType
from app.models.responses import (
    Alert,
    CapacityStatus,
    CutoffInfo,
    DecisionStats,
    ResourceStatus,
    WarehouseStatusResponse,
    WorkloadBreakdown,
)

router = APIRouter()
logger = get_logger(__name__)


@router.get(
    "/status",
    response_model=WarehouseStatusResponse,
    summary="Get warehouse status",
    description="Get comprehensive warehouse status for operational dashboard.",
    tags=["Status"],
)
async def get_warehouse_status(
    # Uncomment for auth: user: User = Depends(require_read_scope)
) -> WarehouseStatusResponse:
    """
    Get comprehensive warehouse status.

    Returns detailed information for operational dashboard including:
    - Current cutoff time and status
    - Workload breakdown by status and priority
    - Capacity utilization by resource type
    - Decision statistics for today
    - Active alerts
    """
    # TODO: Query actual data from HANA
    # This is a mock implementation

    now = datetime.now()
    warehouse_id = "WH-MAIN"

    # Mock cutoff info
    cutoff = CutoffInfo(
        cutoff_time=now.replace(hour=14, minute=30),
        status=DecisionStatus.WARNING,
        trend="INCREASING",
    )

    # Mock workload breakdown
    workload = WorkloadBreakdown(
        total_orders=47,
        total_workload_units=Decimal("523.5"),
        by_status={
            "NEW": 12,
            "PICKING": 18,
            "PACKING": 10,
            "LOADING": 7,
        },
        by_priority={
            "STANDARD": 40,
            "EXPRESS": 5,
            "VIP": 2,
        },
    )

    # Mock capacity status
    capacity = CapacityStatus(
        total_capacity=Decimal("720.0"),
        used_capacity=Decimal("561.6"),
        available_capacity=Decimal("158.4"),
        utilization=Decimal("0.78"),
        bottleneck=ResourceType.PACKER,
        resources={
            "pickers": ResourceStatus(
                available=8, utilization=Decimal("0.75"), efficiency=Decimal("0.92")
            ),
            "packers": ResourceStatus(
                available=5, utilization=Decimal("0.88"), efficiency=Decimal("0.85")
            ),
            "loaders": ResourceStatus(
                available=3, utilization=Decimal("0.60"), efficiency=Decimal("0.95")
            ),
        },
    )

    # Mock decision stats
    decisions = DecisionStats(
        total=285,
        approved=234,
        rejected=51,
        vip_override=8,
        approval_rate=Decimal("0.82"),
    )

    # Mock alerts
    alerts = [
        Alert(
            level=AlertLevel.WARNING,
            code="UTIL_HIGH",
            message="Utilization exceeded 75%",
            timestamp=now.replace(hour=11, minute=45),
        )
    ]

    logger.info("status_retrieved", warehouse_id=warehouse_id)

    return WarehouseStatusResponse(
        timestamp=now,
        warehouse_id=warehouse_id,
        cutoff=cutoff,
        workload=workload,
        capacity=capacity,
        decisions_today=decisions,
        alerts=alerts,
    )
