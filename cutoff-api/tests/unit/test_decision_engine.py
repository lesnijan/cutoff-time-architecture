"""
Unit tests for decision engine.
"""

from decimal import Decimal

import pytest

from app.models.domain import DecisionStatus, Priority
from app.services.capacity_service import CapacityService
from app.services.decision_engine import DecisionEngine
from app.services.workload_calculator import WorkloadCalculator


@pytest.fixture
def decision_engine():
    """Decision engine instance."""
    workload_calc = WorkloadCalculator()
    capacity_service = CapacityService()
    return DecisionEngine(workload_calc, capacity_service)


def test_determine_status_accepting(decision_engine):
    """Test status determination for low utilization."""
    status = decision_engine.determine_status(Decimal("0.65"))
    assert status == DecisionStatus.ACCEPTING


def test_determine_status_warning(decision_engine):
    """Test status determination for medium utilization."""
    status = decision_engine.determine_status(Decimal("0.75"))
    assert status == DecisionStatus.WARNING


def test_determine_status_critical(decision_engine):
    """Test status determination for high utilization."""
    status = decision_engine.determine_status(Decimal("0.90"))
    assert status == DecisionStatus.CRITICAL


def test_determine_status_closed(decision_engine):
    """Test status determination for maximum utilization."""
    status = decision_engine.determine_status(Decimal("0.97"))
    assert status == DecisionStatus.CLOSED


def test_calculate_confidence_low_utilization(decision_engine):
    """Test confidence calculation for low utilization."""
    confidence = decision_engine.calculate_confidence(
        utilization=Decimal("0.50"),
        time_buffer_minutes=60,
        vip_override=False,
    )
    assert confidence > Decimal("0.4")


def test_calculate_confidence_high_utilization(decision_engine):
    """Test confidence calculation for high utilization."""
    confidence = decision_engine.calculate_confidence(
        utilization=Decimal("0.90"),
        time_buffer_minutes=60,
        vip_override=False,
    )
    assert confidence < Decimal("0.2")


def test_calculate_confidence_vip_override(decision_engine):
    """Test confidence calculation with VIP override."""
    confidence_no_vip = decision_engine.calculate_confidence(
        utilization=Decimal("0.70"),
        time_buffer_minutes=60,
        vip_override=False,
    )
    confidence_with_vip = decision_engine.calculate_confidence(
        utilization=Decimal("0.70"),
        time_buffer_minutes=60,
        vip_override=True,
    )
    assert confidence_with_vip < confidence_no_vip


def test_make_decision_can_ship(decision_engine):
    """Test decision making when order can ship today."""
    decision = decision_engine.make_decision(
        new_workload=Decimal("10.0"),
        current_workload=Decimal("100.0"),
        capacity=Decimal("200.0"),
        bottleneck_resource="PACKER",
        priority=Priority.STANDARD,
    )

    assert decision.can_ship_today is True
    assert decision.status in [DecisionStatus.ACCEPTING, DecisionStatus.WARNING]
    assert decision.confidence > Decimal("0.0")


def test_make_decision_cannot_ship(decision_engine):
    """Test decision making when order cannot ship today."""
    decision = decision_engine.make_decision(
        new_workload=Decimal("50.0"),
        current_workload=Decimal("180.0"),
        capacity=Decimal("200.0"),
        bottleneck_resource="PACKER",
        priority=Priority.STANDARD,
    )

    assert decision.can_ship_today is False
    assert decision.status in [DecisionStatus.CRITICAL, DecisionStatus.CLOSED]


def test_make_decision_vip_override(decision_engine):
    """Test VIP priority override."""
    # Standard order that would be rejected
    standard_decision = decision_engine.make_decision(
        new_workload=Decimal("30.0"),
        current_workload=Decimal("170.0"),
        capacity=Decimal("200.0"),
        bottleneck_resource="PACKER",
        priority=Priority.STANDARD,
    )

    # Same order with VIP priority
    vip_decision = decision_engine.make_decision(
        new_workload=Decimal("30.0"),
        current_workload=Decimal("170.0"),
        capacity=Decimal("200.0"),
        bottleneck_resource="PACKER",
        priority=Priority.VIP,
    )

    # VIP should have better chances or at least attempt override
    assert vip_decision.factors.vip_override_used or vip_decision.can_ship_today


def test_calculate_processing_time(decision_engine):
    """Test processing time calculation with congestion."""
    processing_time = decision_engine.calculate_processing_time(
        workload=Decimal("100.0"),
        capacity=Decimal("200.0"),
        utilization=Decimal("0.50"),
    )

    # Should be greater than base time due to congestion factor
    base_time = Decimal("100.0") / Decimal("200.0")
    assert processing_time > base_time
