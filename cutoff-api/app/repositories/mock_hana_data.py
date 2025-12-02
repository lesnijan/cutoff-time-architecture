"""
Mock HANA data for demo purposes.
Simulates realistic warehouse data without actual HANA connection.
"""

import random
from datetime import date, datetime, time, timedelta
from decimal import Decimal
from typing import Any

from app.models.domain import DecisionStatus, OrderStatus

# Demo warehouse configuration
DEMO_WAREHOUSES = {
    "WH-MAIN": {
        "name": "Main Warehouse",
        "pickers": 8,
        "packers": 5,
        "loaders": 3,
        "shift_start": time(6, 0),
        "shift_end": time(16, 0),
    },
    "WH-NORTH": {
        "name": "North Distribution Center",
        "pickers": 12,
        "packers": 8,
        "loaders": 5,
        "shift_start": time(7, 0),
        "shift_end": time(17, 0),
    },
}

# Demo scenarios for different warehouse states
DEMO_SCENARIOS = {
    "normal": {
        "name": "Normal Operations",
        "description": "Standard workload, smooth operations",
        "current_workload": Decimal("280.5"),
        "total_capacity": Decimal("400.0"),
        "utilization": Decimal("0.701"),
        "orders_in_queue": 47,
        "status": DecisionStatus.WARNING,
    },
    "low": {
        "name": "Low Utilization",
        "description": "Light workload, plenty of capacity",
        "current_workload": Decimal("120.0"),
        "total_capacity": Decimal("400.0"),
        "utilization": Decimal("0.30"),
        "orders_in_queue": 18,
        "status": DecisionStatus.ACCEPTING,
    },
    "high": {
        "name": "High Utilization",
        "description": "Heavy workload, near capacity",
        "current_workload": Decimal("360.0"),
        "total_capacity": Decimal("400.0"),
        "utilization": Decimal("0.90"),
        "orders_in_queue": 78,
        "status": DecisionStatus.CRITICAL,
    },
    "overload": {
        "name": "Overloaded",
        "description": "At maximum capacity, rejecting orders",
        "current_workload": Decimal("390.0"),
        "total_capacity": Decimal("400.0"),
        "utilization": Decimal("0.975"),
        "orders_in_queue": 95,
        "status": DecisionStatus.CLOSED,
    },
}

# Demo products with different characteristics
DEMO_PRODUCTS = {
    "MAT-001": {
        "name": "Standard Box - Small",
        "weight_factor": Decimal("1.0"),
        "location_factor": Decimal("1.0"),
        "handling_time": Decimal("0.0"),
    },
    "MAT-002": {
        "name": "Heavy Equipment",
        "weight_factor": Decimal("2.5"),
        "location_factor": Decimal("1.5"),
        "handling_time": Decimal("2.0"),
    },
    "MAT-003": {
        "name": "High Shelf Item",
        "weight_factor": Decimal("1.0"),
        "location_factor": Decimal("1.8"),
        "handling_time": Decimal("1.0"),
    },
    "MAT-004": {
        "name": "Bulk Material",
        "weight_factor": Decimal("3.0"),
        "location_factor": Decimal("1.0"),
        "handling_time": Decimal("3.0"),
    },
    "MAT-005": {
        "name": "Lightweight Package",
        "weight_factor": Decimal("0.5"),
        "location_factor": Decimal("1.0"),
        "handling_time": Decimal("0.0"),
    },
}

# Demo customers
DEMO_CUSTOMERS = {
    "CUST-001": {"name": "ABC Corporation", "is_vip": False, "tier": "STANDARD"},
    "CUST-002": {"name": "XYZ Industries", "is_vip": True, "tier": "VIP"},
    "CUST-003": {"name": "SmallBiz Ltd", "is_vip": False, "tier": "STANDARD"},
    "CUST-VIP-123": {"name": "Premium Client Inc", "is_vip": True, "tier": "VIP"},
}

# Demo orders in various states
DEMO_ORDERS = [
    {
        "order_id": "SO-2024-001",
        "customer_id": "CUST-001",
        "status": OrderStatus.PICKING,
        "created_date": date.today(),
        "items": [
            {"product_id": "MAT-001", "quantity": 10},
            {"product_id": "MAT-003", "quantity": 5},
        ],
    },
    {
        "order_id": "SO-2024-002",
        "customer_id": "CUST-002",
        "status": OrderStatus.NEW,
        "created_date": date.today(),
        "items": [
            {"product_id": "MAT-002", "quantity": 2},
        ],
    },
    {
        "order_id": "SO-2024-003",
        "customer_id": "CUST-003",
        "status": OrderStatus.PACKING,
        "created_date": date.today(),
        "items": [
            {"product_id": "MAT-001", "quantity": 20},
            {"product_id": "MAT-005", "quantity": 50},
        ],
    },
]


class MockHANAData:
    """Mock HANA data provider for demo."""

    def __init__(self, scenario: str = "normal"):
        """
        Initialize mock data with scenario.

        Args:
            scenario: Scenario name (normal, low, high, overload)
        """
        self.scenario = DEMO_SCENARIOS.get(scenario, DEMO_SCENARIOS["normal"])
        self.warehouses = DEMO_WAREHOUSES
        self.products = DEMO_PRODUCTS
        self.customers = DEMO_CUSTOMERS
        self.orders = DEMO_ORDERS

    def get_warehouse_capacity(self, warehouse_id: str = "WH-MAIN") -> dict[str, Any]:
        """Get mock warehouse capacity data."""
        warehouse = self.warehouses.get(warehouse_id, self.warehouses["WH-MAIN"])

        return {
            "available_pickers": warehouse["pickers"],
            "available_packers": warehouse["packers"],
            "available_loaders": warehouse["loaders"],
            "picker_capacity": Decimal(str(warehouse["pickers"] * 1.2)),
            "packer_capacity": Decimal(str(warehouse["packers"] * 0.8)),
            "loader_capacity": Decimal(str(warehouse["loaders"] * 2.0)),
            "usable_capacity": Decimal(str(min(
                warehouse["pickers"] * 1.2,
                warehouse["packers"] * 0.8,
                warehouse["loaders"] * 2.0,
            ) * 0.9)),
        }

    def get_cutoff_calculation(self, warehouse_id: str = "WH-MAIN") -> dict[str, Any]:
        """Get mock cutoff calculation data."""
        return {
            "calc_date": date.today(),
            "calc_time": datetime.now().time(),
            "total_remaining_workload": self.scenario["current_workload"],
            "current_capacity": self.scenario["total_capacity"],
            "current_utilization": self.scenario["utilization"],
            "system_status": self.scenario["status"],
        }

    def get_product_weight_config(self, product_id: str) -> dict[str, Decimal]:
        """Get mock product weight configuration."""
        product = self.products.get(product_id, self.products["MAT-001"])

        return {
            "weight_factor": product["weight_factor"],
            "location_factor": product["location_factor"],
            "handling_time": product["handling_time"],
        }

    def get_orders_by_status(
        self, warehouse_id: str = "WH-MAIN", status: str | None = None
    ) -> list[dict[str, Any]]:
        """Get mock orders filtered by status."""
        orders = []

        for order in self.orders:
            if status is None or order["status"].value == status:
                # Calculate mock workload
                workload = Decimal(str(random.uniform(5.0, 25.0)))

                orders.append({
                    "order_id": order["order_id"],
                    "customer_id": order["customer_id"],
                    "created_date": order["created_date"],
                    "status": order["status"],
                    "workload": workload,
                })

        return orders

    def get_status_breakdown(self) -> dict[str, Any]:
        """Get breakdown of orders by status and priority."""
        # Generate realistic distribution
        total_orders = self.scenario["orders_in_queue"]

        return {
            "by_status": {
                "NEW": int(total_orders * 0.25),
                "PICKING": int(total_orders * 0.38),
                "PACKING": int(total_orders * 0.21),
                "LOADING": int(total_orders * 0.16),
            },
            "by_priority": {
                "STANDARD": int(total_orders * 0.85),
                "EXPRESS": int(total_orders * 0.11),
                "VIP": int(total_orders * 0.04),
            },
        }

    def get_efficiency_profile(self) -> list[dict[str, Any]]:
        """Get time-based efficiency profile for current day."""
        now = datetime.now()
        current_hour = now.hour

        # Efficiency profile throughout the day
        profiles = []
        for hour in range(6, 19):  # 6:00 - 18:00
            if hour < 8:
                efficiency = 0.70  # Rozruch
            elif hour < 12:
                efficiency = 1.00  # Pełna wydajność
            elif hour < 13:
                efficiency = 0.75  # Przerwa obiadowa
            elif hour < 15:
                efficiency = 0.92  # Po przerwie
            elif hour < 17:
                efficiency = 0.82  # Zmęczenie
            else:
                efficiency = 0.65  # Koniec zmiany

            profiles.append({
                "hour": f"{hour:02d}:00",
                "efficiency": efficiency,
                "is_current": hour == current_hour,
            })

        return profiles


# Global mock data instance
_mock_data: MockHANAData | None = None


def get_mock_data(scenario: str = "normal") -> MockHANAData:
    """Get or create mock data instance."""
    global _mock_data
    if _mock_data is None or _mock_data.scenario["name"] != DEMO_SCENARIOS.get(scenario, DEMO_SCENARIOS["normal"])["name"]:
        _mock_data = MockHANAData(scenario)
    return _mock_data


def set_demo_scenario(scenario: str) -> None:
    """Change demo scenario dynamically."""
    global _mock_data
    _mock_data = MockHANAData(scenario)
