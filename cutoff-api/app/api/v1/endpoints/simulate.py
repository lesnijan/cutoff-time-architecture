"""
Simulation endpoint.
POST /simulate - What-if analysis.
"""

from datetime import datetime, timedelta
from decimal import Decimal

from fastapi import APIRouter

from app.core.logging import get_logger
from app.models.domain import DecisionStatus
from app.models.requests import SimulateRequest
from app.models.responses import SimulateResponse, SimulationImpact, SimulationState
from app.services.workload_calculator import get_workload_calculator

router = APIRouter()
logger = get_logger(__name__)


@router.post(
    "/simulate",
    response_model=SimulateResponse,
    summary="Simulate capacity impact",
    description="Perform what-if analysis to predict impact of new orders on capacity.",
    tags=["Simulation"],
)
async def simulate_capacity_impact(
    request: SimulateRequest,
    # Uncomment for auth: user: User = Depends(require_admin_scope)
) -> SimulateResponse:
    """
    Simulate the impact of adding new orders.

    This endpoint allows managers to predict how a batch of orders
    (e.g., flash sale, bulk order) would affect warehouse capacity.
    """
    # TODO: Query current state from HANA
    # Mock current state
    now = datetime.now()
    current_utilization = Decimal("0.78")
    current_cutoff = now.replace(hour=14, minute=30)

    # Calculate additional workload
    workload_calc = get_workload_calculator()
    additional_workload = sum(
        workload_calc.calculate_item_workload(item) for item in request.orders
    )

    # Simulate new state
    # Assuming capacity of 400 units
    total_capacity = Decimal("400.0")
    current_workload = current_utilization * total_capacity
    simulated_workload = current_workload + additional_workload
    simulated_utilization = simulated_workload / total_capacity

    # Calculate impact on cutoff time
    processing_time_increase = float(additional_workload / total_capacity) * 60  # minutes
    simulated_cutoff = current_cutoff - timedelta(minutes=processing_time_increase)

    # Determine simulated status
    if simulated_utilization < Decimal("0.70"):
        simulated_status = DecisionStatus.ACCEPTING
    elif simulated_utilization < Decimal("0.85"):
        simulated_status = DecisionStatus.WARNING
    elif simulated_utilization < Decimal("0.95"):
        simulated_status = DecisionStatus.CRITICAL
    else:
        simulated_status = DecisionStatus.CLOSED

    # Calculate orders at risk
    orders_at_risk = max(0, int((simulated_utilization - Decimal("0.85")) * 100))

    # Generate recommendations
    recommendations = []
    if simulated_utilization > Decimal("0.85"):
        recommendations.append("Consider adding 2 packers")
        recommendations.append("Alert sales team to slow order intake")
    if simulated_utilization > Decimal("0.95"):
        recommendations.append("Prepare overtime authorization")
        recommendations.append("Consider split deliveries for large orders")

    logger.info(
        "simulation_performed",
        scenario=request.scenario_name,
        additional_workload=float(additional_workload),
        simulated_utilization=float(simulated_utilization),
    )

    return SimulateResponse(
        scenario_name=request.scenario_name,
        current_state=SimulationState(
            utilization=current_utilization,
            cutoff_time=current_cutoff,
            status=DecisionStatus.WARNING,
        ),
        simulated_state=SimulationState(
            utilization=simulated_utilization,
            cutoff_time=simulated_cutoff,
            status=simulated_status,
        ),
        impact=SimulationImpact(
            utilization_delta=simulated_utilization - current_utilization,
            cutoff_shift_minutes=-int(processing_time_increase),
            orders_at_risk=orders_at_risk,
        ),
        recommendations=recommendations,
    )
