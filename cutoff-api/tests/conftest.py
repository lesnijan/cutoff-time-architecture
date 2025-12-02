"""
Pytest configuration and fixtures.
"""

from decimal import Decimal

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models.domain import OrderItem, Priority


@pytest.fixture
def client():
    """FastAPI test client."""
    return TestClient(app)


@pytest.fixture
def sample_order_items():
    """Sample order items for testing."""
    return [
        OrderItem(product_id="MAT-001", quantity=10),
        OrderItem(product_id="MAT-002", quantity=5),
        OrderItem(product_id="MAT-003", quantity=3),
    ]


@pytest.fixture
def capacity_check_payload():
    """Sample capacity check request payload."""
    return {
        "order_id": "SO-2024-001234",
        "customer_id": "CUST-5678",
        "priority": "STANDARD",
        "warehouse_id": "WH-MAIN",
        "items": [
            {"product_id": "MAT-001", "quantity": 10},
            {"product_id": "MAT-002", "quantity": 5},
        ],
    }


@pytest.fixture
def vip_capacity_check_payload():
    """Sample VIP capacity check request payload."""
    return {
        "order_id": "SO-2024-VIP-001",
        "customer_id": "CUST-VIP-123",
        "priority": "VIP",
        "warehouse_id": "WH-MAIN",
        "items": [
            {"product_id": "MAT-001", "quantity": 100},
        ],
    }


@pytest.fixture
def simulate_payload():
    """Sample simulation request payload."""
    return {
        "scenario_name": "Flash Sale Impact",
        "warehouse_id": "WH-MAIN",
        "orders": [
            {"product_id": "MAT-001", "quantity": 100},
            {"product_id": "MAT-002", "quantity": 50},
        ],
        "time_horizon_minutes": 60,
    }
