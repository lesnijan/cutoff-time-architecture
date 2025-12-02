"""
Request schemas for API endpoints.
Based on API specification in docs/05-api-specification.md
"""

from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.models.domain import OrderItem, Priority


class CapacityCheckRequest(BaseModel):
    """
    Request schema for POST /capacity/check endpoint.

    Example:
        {
            "order_id": "SO-2024-001234",
            "customer_id": "CUST-5678",
            "priority": "STANDARD",
            "warehouse_id": "WH-MAIN",
            "delivery_date": "2024-01-15",
            "items": [
                {"product_id": "MAT-001", "quantity": 10},
                {"product_id": "MAT-002", "quantity": 5}
            ]
        }
    """

    order_id: Optional[str] = Field(None, description="Order ID for tracking", max_length=50)
    customer_id: Optional[str] = Field(None, description="Customer ID (for VIP check)", max_length=50)
    priority: Priority = Field(default=Priority.STANDARD, description="Order priority level")
    warehouse_id: str = Field(default="WH-MAIN", description="Warehouse identifier", max_length=10)
    delivery_date: Optional[date] = Field(
        None, description="Requested delivery date (defaults to today)"
    )
    items: list[OrderItem] = Field(
        ..., min_length=1, max_length=1000, description="List of order items"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "order_id": "SO-2024-001234",
                "customer_id": "CUST-5678",
                "priority": "STANDARD",
                "warehouse_id": "WH-MAIN",
                "items": [
                    {"product_id": "MAT-001", "quantity": 10},
                    {"product_id": "MAT-002", "quantity": 5},
                ],
            }
        }


class SimulateRequest(BaseModel):
    """
    Request schema for POST /simulate endpoint (what-if analysis).

    Example:
        {
            "scenario_name": "Flash Sale Impact",
            "warehouse_id": "WH-MAIN",
            "orders": [
                {"product_id": "MAT-001", "quantity": 100},
                {"product_id": "MAT-002", "quantity": 50}
            ],
            "time_horizon_minutes": 60
        }
    """

    scenario_name: str = Field(..., description="Name of the scenario", max_length=100)
    warehouse_id: str = Field(default="WH-MAIN", description="Warehouse identifier", max_length=10)
    orders: list[OrderItem] = Field(
        ..., min_length=1, max_length=100, description="Simulated orders"
    )
    time_horizon_minutes: int = Field(
        default=60, ge=5, le=480, description="Simulation time horizon (5-480 min)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "scenario_name": "Flash Sale Impact",
                "warehouse_id": "WH-MAIN",
                "orders": [
                    {"product_id": "MAT-001", "quantity": 100},
                    {"product_id": "MAT-002", "quantity": 50},
                ],
                "time_horizon_minutes": 60,
            }
        }
