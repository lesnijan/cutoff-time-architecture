"""
Capacity service for warehouse capacity calculations.
Based on docs/03-algorithm.md and docs/04-data-model.md
"""

from decimal import Decimal
from typing import Optional

from app.core.logging import get_logger
from app.models.domain import ResourceCapacity, ResourceType, WarehouseCapacity

logger = get_logger(__name__)


class CapacityService:
    """
    Service for calculating warehouse capacity.

    Capacity rates from algorithm spec:
        - Pickers: 1.2 units/min
        - Packers: 0.8 units/min
        - Loaders: 2.0 units/min

    Usable capacity = MIN(picker_cap, packer_cap, loader_cap) × (1 - VIP_reserve)
    """

    # Capacity rates per resource type (units per minute)
    CAPACITY_RATES = {
        ResourceType.PICKER: Decimal("1.2"),
        ResourceType.PACKER: Decimal("0.8"),
        ResourceType.LOADER: Decimal("2.0"),
    }

    def __init__(self, vip_reserve_percent: Decimal = Decimal("0.10")) -> None:
        """
        Initialize capacity service.

        Args:
            vip_reserve_percent: VIP capacity reserve (default 10%)
        """
        self.vip_reserve_percent = vip_reserve_percent

    def calculate_resource_capacity(
        self,
        resource_type: ResourceType,
        available_count: int,
        efficiency: Decimal = Decimal("1.0"),
    ) -> ResourceCapacity:
        """
        Calculate capacity for a specific resource type.

        Args:
            resource_type: Type of resource
            available_count: Number of available resources
            efficiency: Current efficiency factor (0-1)

        Returns:
            ResourceCapacity object
        """
        capacity = ResourceCapacity(
            resource_type=resource_type,
            available_count=available_count,
            base_efficiency=efficiency,
            current_utilization=Decimal("0.0"),
        )

        logger.debug(
            "resource_capacity_calculated",
            resource_type=resource_type.value,
            available_count=available_count,
            capacity_per_minute=float(capacity.capacity_per_minute),
        )

        return capacity

    def calculate_warehouse_capacity(
        self,
        pickers: int,
        packers: int,
        loaders: int,
        picker_efficiency: Decimal = Decimal("1.0"),
        packer_efficiency: Decimal = Decimal("1.0"),
        loader_efficiency: Decimal = Decimal("1.0"),
    ) -> WarehouseCapacity:
        """
        Calculate total warehouse capacity.

        Args:
            pickers: Number of available pickers
            packers: Number of available packers
            loaders: Number of available loaders
            picker_efficiency: Picker efficiency (0-1)
            packer_efficiency: Packer efficiency (0-1)
            loader_efficiency: Loader efficiency (0-1)

        Returns:
            WarehouseCapacity object
        """
        picker_capacity = self.calculate_resource_capacity(
            ResourceType.PICKER, pickers, picker_efficiency
        )
        packer_capacity = self.calculate_resource_capacity(
            ResourceType.PACKER, packers, packer_efficiency
        )
        loader_capacity = self.calculate_resource_capacity(
            ResourceType.LOADER, loaders, loader_efficiency
        )

        warehouse_capacity = WarehouseCapacity(
            picker_capacity=picker_capacity,
            packer_capacity=packer_capacity,
            loader_capacity=loader_capacity,
            vip_reserve_percent=self.vip_reserve_percent,
        )

        logger.info(
            "warehouse_capacity_calculated",
            pickers=pickers,
            packers=packers,
            loaders=loaders,
            bottleneck=warehouse_capacity.bottleneck_resource.value,
            usable_capacity=float(warehouse_capacity.usable_capacity),
        )

        return warehouse_capacity

    def calculate_utilization(
        self, current_workload: Decimal, capacity: Decimal
    ) -> Decimal:
        """
        Calculate current utilization percentage.

        Args:
            current_workload: Current workload in minutes
            capacity: Available capacity in minutes

        Returns:
            Utilization as decimal (0-1)
        """
        if capacity <= 0:
            logger.warning("zero_capacity", capacity=float(capacity))
            return Decimal("1.0")

        utilization = current_workload / capacity

        logger.debug(
            "utilization_calculated",
            workload=float(current_workload),
            capacity=float(capacity),
            utilization=float(utilization),
        )

        return utilization

    def get_remaining_capacity(
        self, total_capacity: Decimal, current_workload: Decimal
    ) -> Decimal:
        """
        Calculate remaining available capacity.

        Args:
            total_capacity: Total capacity in minutes
            current_workload: Current workload in minutes

        Returns:
            Remaining capacity in minutes
        """
        remaining = max(Decimal("0.0"), total_capacity - current_workload)

        logger.debug(
            "remaining_capacity_calculated",
            total_capacity=float(total_capacity),
            current_workload=float(current_workload),
            remaining=float(remaining),
        )

        return remaining

    def can_accommodate_workload(
        self,
        new_workload: Decimal,
        current_workload: Decimal,
        capacity: Decimal,
        max_utilization: Decimal = Decimal("0.85"),
    ) -> tuple[bool, Decimal]:
        """
        Check if warehouse can accommodate additional workload.

        Args:
            new_workload: New workload to add (minutes)
            current_workload: Current workload (minutes)
            capacity: Available capacity (minutes)
            max_utilization: Maximum allowed utilization (default 0.85)

        Returns:
            Tuple of (can_accommodate, resulting_utilization)
        """
        projected_workload = current_workload + new_workload
        projected_utilization = self.calculate_utilization(projected_workload, capacity)

        can_accommodate = projected_utilization <= max_utilization

        logger.info(
            "accommodation_check",
            new_workload=float(new_workload),
            current_workload=float(current_workload),
            capacity=float(capacity),
            projected_utilization=float(projected_utilization),
            max_utilization=float(max_utilization),
            can_accommodate=can_accommodate,
        )

        return can_accommodate, projected_utilization


# Global service instance
_capacity_service: Optional[CapacityService] = None


def get_capacity_service() -> CapacityService:
    """Get global capacity service instance."""
    global _capacity_service
    if _capacity_service is None:
        _capacity_service = CapacityService()
    return _capacity_service
