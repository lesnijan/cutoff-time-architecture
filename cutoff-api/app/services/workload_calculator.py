"""
Workload calculator service.
Implements formulas from docs/03-algorithm.md
"""

from decimal import Decimal
from typing import Optional

from app.core.logging import get_logger
from app.models.domain import Order, OrderItem, OrderStatus, Workload

logger = get_logger(__name__)


class WorkloadCalculator:
    """
    Calculate workload for orders based on algorithm specification.

    Formula from docs:
        W_order = Σ(quantity × weight_factor × location_factor) + S + P + L

    Where:
        - S = setup_time (2 min)
        - P = packing_base (3 min) + (item_count × 0.5 min)
        - L = loading_time (1.5 min)
    """

    # Constants from algorithm specification
    SETUP_TIME = Decimal("2.0")  # minutes
    PACKING_BASE = Decimal("3.0")  # minutes
    PACKING_PER_ITEM = Decimal("0.5")  # minutes per item
    LOADING_TIME = Decimal("1.5")  # minutes

    # Progress factors by status (from algorithm spec)
    PROGRESS_FACTORS = {
        OrderStatus.NEW: Decimal("1.00"),
        OrderStatus.ALLOCATED: Decimal("0.95"),
        OrderStatus.PICKING: Decimal("0.60"),
        OrderStatus.PACKING: Decimal("0.25"),
        OrderStatus.LOADING: Decimal("0.08"),
        OrderStatus.SHIPPED: Decimal("0.00"),
    }

    def calculate_item_workload(self, item: OrderItem) -> Decimal:
        """
        Calculate workload for a single item.

        Args:
            item: Order item

        Returns:
            Item workload in minutes
        """
        weight_factor = item.weight_factor or Decimal("1.0")
        location_factor = item.location_factor or Decimal("1.0")

        workload = Decimal(item.quantity) * weight_factor * location_factor

        logger.debug(
            "item_workload_calculated",
            product_id=item.product_id,
            quantity=item.quantity,
            weight_factor=float(weight_factor),
            location_factor=float(location_factor),
            workload=float(workload),
        )

        return workload

    def calculate_order_workload(
        self,
        items: list[OrderItem],
        status: Optional[OrderStatus] = None,
    ) -> Workload:
        """
        Calculate total workload for an order.

        Args:
            items: List of order items
            status: Order status (affects progress factor)

        Returns:
            Workload object with breakdown
        """
        # Calculate item workloads
        item_workload = sum(
            (self.calculate_item_workload(item) for item in items),
            start=Decimal("0.0"),
        )

        # Calculate packing time based on item count
        packing_time = self.PACKING_BASE + (Decimal(len(items)) * self.PACKING_PER_ITEM)

        # Total workload
        total = item_workload + self.SETUP_TIME + packing_time + self.LOADING_TIME

        # Apply progress factor if status provided
        progress_factor = self.PROGRESS_FACTORS.get(status, Decimal("1.0")) if status else Decimal("1.0")
        remaining = total * progress_factor

        logger.info(
            "order_workload_calculated",
            item_count=len(items),
            item_workload=float(item_workload),
            setup=float(self.SETUP_TIME),
            packing=float(packing_time),
            loading=float(self.LOADING_TIME),
            total=float(total),
            progress_factor=float(progress_factor),
            remaining=float(remaining),
        )

        return Workload(
            item_workload=item_workload,
            setup_time=self.SETUP_TIME,
            packing_base=self.PACKING_BASE,
            packing_per_item=self.PACKING_PER_ITEM,
            loading_time=self.LOADING_TIME,
        )

    def calculate_batch_workload(self, orders: list[Order]) -> Decimal:
        """
        Calculate total workload for multiple orders.

        Args:
            orders: List of orders

        Returns:
            Total workload in minutes
        """
        total = Decimal("0.0")

        for order in orders:
            workload = self.calculate_order_workload(order.items)
            total += workload.total_workload

        logger.info(
            "batch_workload_calculated",
            order_count=len(orders),
            total_workload=float(total),
        )

        return total

    def calculate_congestion_factor(
        self, utilization: Decimal, alpha: Decimal = Decimal("1.2")
    ) -> Decimal:
        """
        Calculate congestion factor based on utilization.

        Formula from docs:
            CONGESTION_FACTOR = 1 + α × UTILIZATION²

        Args:
            utilization: Current utilization (0-1)
            alpha: Congestion coefficient (default 1.2)

        Returns:
            Congestion factor (≥ 1.0)
        """
        congestion = Decimal("1.0") + (alpha * (utilization ** 2))

        logger.debug(
            "congestion_calculated",
            utilization=float(utilization),
            alpha=float(alpha),
            congestion_factor=float(congestion),
        )

        return congestion


# Global service instance
_workload_calculator: Optional[WorkloadCalculator] = None


def get_workload_calculator() -> WorkloadCalculator:
    """Get global workload calculator instance."""
    global _workload_calculator
    if _workload_calculator is None:
        _workload_calculator = WorkloadCalculator()
    return _workload_calculator
