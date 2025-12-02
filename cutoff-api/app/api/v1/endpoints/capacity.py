"""
Capacity check endpoint.
POST /capacity/check - Main decision endpoint.
"""

import time
from datetime import datetime
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException

from app.core.logging import get_logger
from app.core.metrics import capacity_checks_total
from app.models.domain import ResourceType
from app.models.requests import CapacityCheckRequest
from app.models.responses import CalculationMetadata, CapacityCheckResponse
from app.repositories.cache_repository import get_cache_repository
from app.repositories.hana_repository import get_hana_repository
from app.services.capacity_service import get_capacity_service
from app.services.decision_engine import get_decision_engine
from app.services.workload_calculator import get_workload_calculator

router = APIRouter()
logger = get_logger(__name__)


@router.post(
    "/capacity/check",
    response_model=CapacityCheckResponse,
    summary="Check if order can ship today",
    description="Check warehouse capacity and determine if new order can be shipped today.",
    tags=["Capacity"],
)
async def check_capacity(
    request: CapacityCheckRequest,
    # Uncomment for auth: user: User = Depends(require_write_scope)
) -> CapacityCheckResponse:
    """
    Check warehouse capacity for a new order.

    This endpoint:
    1. Calculates workload for the order
    2. Queries current warehouse capacity from HANA
    3. Applies decision logic
    4. Returns decision with factors

    Response is cached for 60 seconds.
    """
    start_time = time.time()
    cache_hit = False

    # Try to get cached result
    cache_repo = get_cache_repository()
    cached_decision = await cache_repo.get_cached_decision(request)

    if cached_decision:
        cache_hit = True
        calc_time_ms = int((time.time() - start_time) * 1000)

        logger.info(
            "capacity_check_cached",
            warehouse_id=request.warehouse_id,
            priority=request.priority.value,
            item_count=len(request.items),
            decision=cached_decision.can_ship_today,
        )

        return CapacityCheckResponse(
            can_ship_today=cached_decision.can_ship_today,
            confidence=cached_decision.confidence,
            estimated_completion=cached_decision.estimated_completion,
            current_utilization=cached_decision.current_utilization,
            message=cached_decision.message,
            decision_factors=cached_decision.factors,
            metadata=CalculationMetadata(
                calculated_at=cached_decision.calculated_at,
                cache_hit=True,
                calculation_time_ms=calc_time_ms,
            ),
        )

    # Calculate workload
    workload_calc = get_workload_calculator()
    workload = workload_calc.calculate_order_workload(request.items)

    logger.info(
        "order_workload_calculated",
        order_id=request.order_id,
        total_workload=float(workload.total_workload),
    )

    # Get current warehouse capacity from HANA
    hana_repo = get_hana_repository()
    try:
        capacity_data = await hana_repo.get_current_warehouse_capacity(request.warehouse_id)
    except Exception as e:
        logger.error("hana_query_failed", error=str(e))
        raise HTTPException(
            status_code=503,
            detail="Failed to query warehouse capacity from database",
        )

    # Build capacity object
    capacity_service = get_capacity_service()
    warehouse_capacity = capacity_service.calculate_warehouse_capacity(
        pickers=capacity_data["available_pickers"],
        packers=capacity_data["available_packers"],
        loaders=capacity_data["available_loaders"],
    )

    # Get current workload from HANA
    try:
        cutoff_data = await hana_repo.get_cutoff_calculation(request.warehouse_id)
        current_workload = cutoff_data["total_remaining_workload"]
    except Exception as e:
        logger.error("hana_cutoff_query_failed", error=str(e))
        current_workload = Decimal("0.0")

    # Make decision
    decision_engine = get_decision_engine()
    decision = decision_engine.make_decision(
        new_workload=workload.total_workload,
        current_workload=current_workload,
        capacity=warehouse_capacity.usable_capacity,
        bottleneck_resource=warehouse_capacity.bottleneck_resource.value,
        priority=request.priority,
    )

    # Cache decision
    await cache_repo.cache_decision(request, decision)

    # Record metrics
    capacity_checks_total.labels(
        decision="approved" if decision.can_ship_today else "rejected",
        priority=request.priority.value,
    ).inc()

    calc_time_ms = int((time.time() - start_time) * 1000)

    logger.info(
        "capacity_check_completed",
        warehouse_id=request.warehouse_id,
        order_id=request.order_id,
        decision=decision.can_ship_today,
        utilization=float(decision.current_utilization),
        calc_time_ms=calc_time_ms,
    )

    return CapacityCheckResponse(
        can_ship_today=decision.can_ship_today,
        confidence=decision.confidence,
        estimated_completion=decision.estimated_completion,
        current_utilization=decision.current_utilization,
        message=decision.message,
        decision_factors=decision.factors,
        metadata=CalculationMetadata(
            calculated_at=decision.calculated_at,
            cache_hit=False,
            calculation_time_ms=calc_time_ms,
        ),
    )
