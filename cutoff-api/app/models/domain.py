"""
Domain models for Cutoff Time System.
Based on algorithm specification in docs/03-algorithm.md
"""

from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class Priority(str, Enum):
    """Order priority levels."""

    STANDARD = "STANDARD"
    EXPRESS = "EXPRESS"
    VIP = "VIP"


class DecisionStatus(str, Enum):
    """Warehouse operational status based on utilization."""

    ACCEPTING = "ACCEPTING"  # < 70% utilization
    WARNING = "WARNING"  # 70-85% utilization
    CRITICAL = "CRITICAL"  # 85-95% utilization
    CLOSED = "CLOSED"  # > 95% utilization


class AlertLevel(str, Enum):
    """Alert severity levels."""

    NONE = "NONE"
    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"


class OrderStatus(str, Enum):
    """Order processing status with progress factors."""

    NEW = "NEW"  # Factor: 1.00
    ALLOCATED = "ALLOCATED"  # Factor: 0.95
    PICKING = "PICKING"  # Factor: 0.60
    PACKING = "PACKING"  # Factor: 0.25
    LOADING = "LOADING"  # Factor: 0.08
    SHIPPED = "SHIPPED"  # Factor: 0.00


class ResourceType(str, Enum):
    """Warehouse resource types."""

    PICKER = "PICKER"
    PACKER = "PACKER"
    LOADER = "LOADER"


class OrderItem(BaseModel):
    """Single item in an order."""

    model_config = ConfigDict(frozen=True)

    product_id: str = Field(..., description="Material/Product ID (MATNR)")
    quantity: int = Field(..., gt=0, description="Order quantity")
    weight_factor: Optional[Decimal] = Field(
        default=Decimal("1.0"),
        ge=Decimal("1.0"),
        le=Decimal("3.0"),
        description="Product workload weight factor",
    )
    location_factor: Optional[Decimal] = Field(
        default=Decimal("1.0"),
        ge=Decimal("1.0"),
        le=Decimal("2.0"),
        description="Storage location difficulty factor",
    )


class Order(BaseModel):
    """Complete order with metadata."""

    order_id: Optional[str] = Field(None, description="Sales order number (VBELN)")
    customer_id: Optional[str] = Field(None, description="Customer number (KUNNR)")
    priority: Priority = Field(default=Priority.STANDARD, description="Order priority")
    items: list[OrderItem] = Field(..., min_length=1, description="Order line items")
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Workload(BaseModel):
    """Calculated workload for an order or warehouse."""

    item_workload: Decimal = Field(
        default=Decimal("0.0"), ge=0, description="Sum of item workloads"
    )
    setup_time: Decimal = Field(default=Decimal("2.0"), description="Setup time (min)")
    packing_base: Decimal = Field(default=Decimal("3.0"), description="Base packing time (min)")
    packing_per_item: Decimal = Field(
        default=Decimal("0.5"), description="Additional packing per item (min)"
    )
    loading_time: Decimal = Field(default=Decimal("1.5"), description="Loading time (min)")

    @property
    def total_workload(self) -> Decimal:
        """Calculate total workload in minutes."""
        return (
            self.item_workload
            + self.setup_time
            + self.packing_base
            + self.loading_time
        )


class ResourceCapacity(BaseModel):
    """Capacity for a specific resource type."""

    resource_type: ResourceType
    available_count: int = Field(..., ge=0, description="Number of available resources")
    base_efficiency: Decimal = Field(
        default=Decimal("1.0"), ge=0, le=1, description="Base efficiency (0-1)"
    )
    current_utilization: Decimal = Field(
        default=Decimal("0.0"), ge=0, le=1, description="Current utilization (0-1)"
    )

    @property
    def capacity_per_minute(self) -> Decimal:
        """Calculate capacity per minute based on resource type."""
        rates = {
            ResourceType.PICKER: Decimal("1.2"),
            ResourceType.PACKER: Decimal("0.8"),
            ResourceType.LOADER: Decimal("2.0"),
        }
        return Decimal(self.available_count) * rates[self.resource_type]


class WarehouseCapacity(BaseModel):
    """Total warehouse capacity across all resources."""

    picker_capacity: ResourceCapacity
    packer_capacity: ResourceCapacity
    loader_capacity: ResourceCapacity
    vip_reserve_percent: Decimal = Field(
        default=Decimal("0.10"), ge=0, le=0.3, description="VIP reserve (default 10%)"
    )

    @property
    def bottleneck_resource(self) -> ResourceType:
        """Identify the bottleneck resource (minimum capacity)."""
        capacities = {
            ResourceType.PICKER: self.picker_capacity.capacity_per_minute,
            ResourceType.PACKER: self.packer_capacity.capacity_per_minute,
            ResourceType.LOADER: self.loader_capacity.capacity_per_minute,
        }
        return min(capacities, key=capacities.get)  # type: ignore

    @property
    def usable_capacity(self) -> Decimal:
        """Calculate usable capacity (bottleneck - VIP reserve)."""
        capacities = [
            self.picker_capacity.capacity_per_minute,
            self.packer_capacity.capacity_per_minute,
            self.loader_capacity.capacity_per_minute,
        ]
        min_capacity = min(capacities)
        return min_capacity * (Decimal("1.0") - self.vip_reserve_percent)


class DecisionFactors(BaseModel):
    """Factors influencing the capacity decision."""

    workload_impact: Decimal = Field(..., description="Workload impact (minutes)")
    remaining_capacity: Decimal = Field(..., description="Remaining capacity (minutes)")
    time_buffer_minutes: int = Field(..., description="Safety buffer (minutes)")
    bottleneck_resource: ResourceType = Field(..., description="Current bottleneck")
    congestion_factor: Decimal = Field(
        default=Decimal("1.0"), ge=1, description="Congestion multiplier"
    )
    vip_override_used: bool = Field(
        default=False, description="Whether VIP reserve was used"
    )


class Decision(BaseModel):
    """Capacity check decision with metadata."""

    can_ship_today: bool = Field(..., description="Whether order can ship today")
    status: DecisionStatus = Field(..., description="Warehouse status")
    confidence: Decimal = Field(..., ge=0, le=1, description="Decision confidence (0-1)")
    current_utilization: Decimal = Field(..., ge=0, description="Current utilization (0-1)")
    estimated_completion: datetime = Field(..., description="Estimated completion time")
    message: str = Field(..., description="Human-readable decision message")
    factors: DecisionFactors = Field(..., description="Decision factors")
    calculated_at: datetime = Field(default_factory=datetime.utcnow)
