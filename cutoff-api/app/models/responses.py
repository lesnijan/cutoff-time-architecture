"""
Response schemas for API endpoints.
Based on API specification in docs/05-api-specification.md
"""

from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field

from app.models.domain import AlertLevel, DecisionFactors, DecisionStatus, ResourceType


class CalculationMetadata(BaseModel):
    """Metadata about the calculation."""

    calculated_at: datetime = Field(..., description="Timestamp of calculation")
    cache_hit: bool = Field(..., description="Whether result was cached")
    calculation_time_ms: int = Field(..., description="Calculation time in milliseconds")
    request_id: Optional[str] = Field(None, description="Request tracking ID")


class Alternative(BaseModel):
    """Alternative option when order cannot ship today."""

    option: str = Field(..., description="Alternative option code")
    description: str = Field(..., description="Human-readable description")
    available: bool = Field(default=True, description="Whether option is available")
    items_today: Optional[int] = Field(None, description="Items that can ship today (if split)")
    items_tomorrow: Optional[int] = Field(None, description="Items for tomorrow (if split)")


class CapacityCheckResponse(BaseModel):
    """
    Response schema for POST /capacity/check endpoint.

    Example (Success):
        {
            "can_ship_today": true,
            "confidence": 0.92,
            "estimated_completion": "2024-01-15T15:30:00Z",
            "current_utilization": 0.72,
            "message": "Wysyłka dziś możliwa ✓",
            "decision_factors": {...},
            "metadata": {...}
        }
    """

    can_ship_today: bool = Field(..., description="Whether order can ship today")
    confidence: Decimal = Field(..., ge=0, le=1, description="Decision confidence (0-1)")
    estimated_completion: datetime = Field(..., description="Estimated completion time")
    current_utilization: Decimal = Field(..., ge=0, description="Current warehouse utilization")
    message: str = Field(..., description="Human-readable decision message")
    decision_factors: DecisionFactors = Field(..., description="Factors influencing decision")
    metadata: CalculationMetadata = Field(..., description="Calculation metadata")

    # Optional fields for rejection scenarios
    reason: Optional[str] = Field(None, description="Rejection reason code")
    next_available_slot: Optional[datetime] = Field(None, description="Next available time slot")
    alternatives: Optional[list[Alternative]] = Field(None, description="Alternative options")

    class Config:
        json_schema_extra = {
            "example": {
                "can_ship_today": True,
                "confidence": 0.92,
                "estimated_completion": "2024-01-15T15:30:00Z",
                "current_utilization": 0.72,
                "message": "Wysyłka dziś możliwa ✓",
                "decision_factors": {
                    "workload_impact": 12.5,
                    "remaining_capacity": 45.2,
                    "time_buffer_minutes": 30,
                    "bottleneck_resource": "PACKERS",
                },
                "metadata": {
                    "calculated_at": "2024-01-15T12:00:00Z",
                    "cache_hit": False,
                    "calculation_time_ms": 45,
                },
            }
        }


class StatusHistoryPoint(BaseModel):
    """Single point in status history."""

    time: str = Field(..., description="Time (HH:MM format)")
    status: DecisionStatus = Field(..., description="Status at that time")
    utilization: Decimal = Field(..., ge=0, le=1, description="Utilization at that time")


class CutoffStatusResponse(BaseModel):
    """
    Response schema for GET /cutoff/current endpoint.

    Example:
        {
            "cutoff_time": "2024-01-15T14:30:00Z",
            "hard_deadline": "2024-01-15T16:00:00Z",
            "current_time": "2024-01-15T12:00:00Z",
            "time_remaining_minutes": 150,
            "current_utilization": 0.78,
            "orders_in_queue": 47,
            "estimated_orders_remaining": 12,
            "status": "WARNING",
            "trend": "INCREASING",
            "alert_level": "YELLOW"
        }
    """

    cutoff_time: datetime = Field(..., description="Current dynamic cutoff time")
    hard_deadline: datetime = Field(..., description="Hard deadline (end of shift)")
    current_time: datetime = Field(..., description="Current server time")
    time_remaining_minutes: int = Field(..., description="Minutes until cutoff")
    current_utilization: Decimal = Field(..., ge=0, description="Current utilization")
    orders_in_queue: int = Field(..., ge=0, description="Orders currently in queue")
    estimated_orders_remaining: int = Field(..., ge=0, description="Estimated remaining capacity")
    status: DecisionStatus = Field(..., description="Current warehouse status")
    trend: str = Field(..., description="Trend: INCREASING, STABLE, DECREASING")
    alert_level: AlertLevel = Field(..., description="Alert level")
    status_history: Optional[list[StatusHistoryPoint]] = Field(
        None, description="Status history (last 3-5 points)"
    )


class ResourceStatus(BaseModel):
    """Status of a specific resource type."""

    available: int = Field(..., ge=0, description="Number of available resources")
    utilization: Decimal = Field(..., ge=0, le=1, description="Current utilization")
    efficiency: Decimal = Field(..., ge=0, le=1, description="Current efficiency")


class WorkloadBreakdown(BaseModel):
    """Breakdown of workload by status or priority."""

    total_orders: int = Field(..., ge=0, description="Total number of orders")
    total_workload_units: Decimal = Field(..., ge=0, description="Total workload in units")
    by_status: dict[str, int] = Field(..., description="Orders by status")
    by_priority: dict[str, int] = Field(..., description="Orders by priority")


class CapacityStatus(BaseModel):
    """Current capacity status."""

    total_capacity: Decimal = Field(..., ge=0, description="Total capacity")
    used_capacity: Decimal = Field(..., ge=0, description="Used capacity")
    available_capacity: Decimal = Field(..., ge=0, description="Available capacity")
    utilization: Decimal = Field(..., ge=0, le=1, description="Utilization percentage")
    bottleneck: ResourceType = Field(..., description="Current bottleneck resource")
    resources: dict[str, ResourceStatus] = Field(..., description="Status by resource type")


class CutoffInfo(BaseModel):
    """Cutoff time information."""

    cutoff_time: datetime = Field(..., description="Current cutoff time")
    status: DecisionStatus = Field(..., description="Current status")
    trend: str = Field(..., description="Trend direction")


class DecisionStats(BaseModel):
    """Statistics about decisions made today."""

    total: int = Field(..., ge=0, description="Total decisions")
    approved: int = Field(..., ge=0, description="Approved orders")
    rejected: int = Field(..., ge=0, description="Rejected orders")
    vip_override: int = Field(..., ge=0, description="VIP overrides")
    approval_rate: Decimal = Field(..., ge=0, le=1, description="Approval rate")


class Alert(BaseModel):
    """Alert message."""

    level: AlertLevel = Field(..., description="Alert level")
    code: str = Field(..., description="Alert code")
    message: str = Field(..., description="Alert message")
    timestamp: datetime = Field(..., description="Alert timestamp")


class WarehouseStatusResponse(BaseModel):
    """
    Response schema for GET /status endpoint.
    Comprehensive dashboard data.
    """

    timestamp: datetime = Field(..., description="Response timestamp")
    warehouse_id: str = Field(..., description="Warehouse identifier")
    cutoff: CutoffInfo = Field(..., description="Cutoff information")
    workload: WorkloadBreakdown = Field(..., description="Workload breakdown")
    capacity: CapacityStatus = Field(..., description="Capacity status")
    decisions_today: DecisionStats = Field(..., description="Decision statistics")
    alerts: list[Alert] = Field(default_factory=list, description="Active alerts")


class SimulationState(BaseModel):
    """State snapshot for simulation."""

    utilization: Decimal = Field(..., ge=0, description="Utilization")
    cutoff_time: datetime = Field(..., description="Cutoff time")
    status: Optional[DecisionStatus] = Field(None, description="Status")


class SimulationImpact(BaseModel):
    """Impact metrics of simulation."""

    utilization_delta: Decimal = Field(..., description="Change in utilization")
    cutoff_shift_minutes: int = Field(..., description="Cutoff time shift (negative = earlier)")
    orders_at_risk: int = Field(..., ge=0, description="Orders at risk")


class SimulateResponse(BaseModel):
    """Response schema for POST /simulate endpoint."""

    scenario_name: str = Field(..., description="Scenario name")
    current_state: SimulationState = Field(..., description="Current state")
    simulated_state: SimulationState = Field(..., description="Simulated state")
    impact: SimulationImpact = Field(..., description="Impact analysis")
    recommendations: list[str] = Field(..., description="Recommendations")


class HealthCheck(BaseModel):
    """Health check status."""

    component: str = Field(..., description="Component name")
    status: str = Field(..., description="Status: ok, degraded, down")
    message: Optional[str] = Field(None, description="Additional message")


class HealthResponse(BaseModel):
    """Response schema for GET /health endpoint."""

    status: str = Field(..., description="Overall status: healthy, degraded, unhealthy")
    version: str = Field(..., description="API version")
    timestamp: datetime = Field(..., description="Health check timestamp")
    checks: dict[str, str] = Field(..., description="Component health statuses")
    uptime_seconds: int = Field(..., ge=0, description="Uptime in seconds")


class ErrorDetail(BaseModel):
    """Error detail for validation errors."""

    field: str = Field(..., description="Field name")
    error: str = Field(..., description="Error message")


class ErrorResponse(BaseModel):
    """Standard error response."""

    error: str = Field(..., description="Error code")
    message: str = Field(..., description="Error message")
    details: Optional[list[ErrorDetail]] = Field(None, description="Validation errors")
    request_id: Optional[str] = Field(None, description="Request tracking ID")
    retry_after_seconds: Optional[int] = Field(None, description="Retry after (for rate limit)")
    limit: Optional[str] = Field(None, description="Rate limit description")
