"""
Decision engine - core business logic for capacity decisions.
Implements algorithm from docs/03-algorithm.md
"""

from datetime import datetime, timedelta
from decimal import Decimal
from typing import Optional

from app.config import get_settings
from app.core.logging import get_logger
from app.models.domain import Decision, DecisionFactors, DecisionStatus, Priority
from app.services.capacity_service import CapacityService
from app.services.workload_calculator import WorkloadCalculator

logger = get_logger(__name__)


class DecisionEngine:
    """
    Core decision engine for cutoff time calculations.

    Decision logic from algorithm spec:
        IF (UTILIZATION < 0.85) AND (current_time + PROC_TIME < deadline - buffer)
        THEN → "Ship Today" ✓
        ELSE → "Ship Tomorrow" ✗

    Processing time calculation:
        PROC_TIME = (WORKLOAD / CAPACITY) × CONGESTION_FACTOR

    Congestion factor:
        CONGESTION_FACTOR = 1 + α × UTILIZATION²
    """

    def __init__(
        self,
        workload_calculator: WorkloadCalculator,
        capacity_service: CapacityService,
    ) -> None:
        """
        Initialize decision engine.

        Args:
            workload_calculator: Workload calculation service
            capacity_service: Capacity calculation service
        """
        self.workload_calculator = workload_calculator
        self.capacity_service = capacity_service
        self.settings = get_settings()

    def calculate_processing_time(
        self, workload: Decimal, capacity: Decimal, utilization: Decimal
    ) -> Decimal:
        """
        Calculate processing time with congestion factor.

        Args:
            workload: Workload in minutes
            capacity: Capacity in units/minute
            utilization: Current utilization (0-1)

        Returns:
            Processing time in minutes
        """
        congestion_factor = self.workload_calculator.calculate_congestion_factor(
            utilization, Decimal(str(self.settings.congestion_alpha))
        )

        base_time = workload / capacity if capacity > 0 else workload
        processing_time = base_time * congestion_factor

        logger.debug(
            "processing_time_calculated",
            workload=float(workload),
            capacity=float(capacity),
            utilization=float(utilization),
            congestion_factor=float(congestion_factor),
            processing_time=float(processing_time),
        )

        return processing_time

    def determine_status(self, utilization: Decimal) -> DecisionStatus:
        """
        Determine warehouse status based on utilization.

        Thresholds from algorithm spec:
            - < 70% → ACCEPTING
            - 70-85% → WARNING
            - 85-95% → CRITICAL
            - > 95% → CLOSED

        Args:
            utilization: Current utilization (0-1)

        Returns:
            DecisionStatus
        """
        if utilization < Decimal("0.70"):
            return DecisionStatus.ACCEPTING
        elif utilization < Decimal("0.85"):
            return DecisionStatus.WARNING
        elif utilization < Decimal("0.95"):
            return DecisionStatus.CRITICAL
        else:
            return DecisionStatus.CLOSED

    def calculate_confidence(
        self,
        utilization: Decimal,
        time_buffer_minutes: int,
        vip_override: bool = False,
    ) -> Decimal:
        """
        Calculate confidence score for the decision.

        Args:
            utilization: Current utilization
            time_buffer_minutes: Time buffer until deadline
            vip_override: Whether VIP override was used

        Returns:
            Confidence score (0-1)
        """
        # Base confidence from utilization (inverse relationship)
        base_confidence = Decimal("1.0") - utilization

        # Adjust for time buffer
        if time_buffer_minutes < 15:
            base_confidence *= Decimal("0.7")
        elif time_buffer_minutes < 30:
            base_confidence *= Decimal("0.85")

        # Reduce confidence if VIP override used
        if vip_override:
            base_confidence *= Decimal("0.80")

        # Clamp to [0, 1]
        confidence = max(Decimal("0.0"), min(Decimal("1.0"), base_confidence))

        logger.debug(
            "confidence_calculated",
            utilization=float(utilization),
            time_buffer=time_buffer_minutes,
            vip_override=vip_override,
            confidence=float(confidence),
        )

        return confidence

    def make_decision(
        self,
        new_workload: Decimal,
        current_workload: Decimal,
        capacity: Decimal,
        bottleneck_resource: str,
        priority: Priority = Priority.STANDARD,
        deadline: Optional[datetime] = None,
    ) -> Decision:
        """
        Make capacity decision for a new order.

        Args:
            new_workload: Workload of new order (minutes)
            current_workload: Current warehouse workload (minutes)
            capacity: Available capacity (units/minute)
            bottleneck_resource: Current bottleneck resource type
            priority: Order priority
            deadline: Deadline for completion (defaults to end of shift)

        Returns:
            Decision object
        """
        # Set default deadline (end of shift at 16:00)
        if deadline is None:
            now = datetime.now()
            deadline = now.replace(hour=16, minute=0, second=0, microsecond=0)
            if now >= deadline:
                deadline += timedelta(days=1)

        # Calculate projected utilization
        projected_workload = current_workload + new_workload
        current_utilization = self.capacity_service.calculate_utilization(
            current_workload, capacity
        )
        projected_utilization = self.capacity_service.calculate_utilization(
            projected_workload, capacity
        )

        # Calculate processing time
        processing_time = self.calculate_processing_time(
            projected_workload, capacity, projected_utilization
        )

        # Estimate completion time
        estimated_completion = datetime.now() + timedelta(minutes=float(processing_time))

        # Calculate time buffer
        time_remaining = (deadline - datetime.now()).total_seconds() / 60
        safety_buffer = self.settings.safety_buffer_minutes
        time_buffer = int(time_remaining - float(processing_time))

        # Determine if can ship today
        max_utilization = Decimal(str(self.settings.max_utilization))
        utilization_ok = projected_utilization < max_utilization
        time_ok = time_buffer >= safety_buffer

        # Check for VIP override
        vip_override = False
        if priority == Priority.VIP and not (utilization_ok and time_ok):
            # VIP can use reserve capacity
            vip_utilization_threshold = max_utilization + Decimal("0.10")
            if projected_utilization < vip_utilization_threshold:
                utilization_ok = True
                vip_override = True
                logger.info("vip_override_applied", utilization=float(projected_utilization))

        can_ship_today = utilization_ok and time_ok

        # Determine status and message
        status = self.determine_status(projected_utilization)

        if can_ship_today:
            message = "Wysyłka dziś możliwa ✓"
        else:
            if not utilization_ok:
                message = "Wysyłka jutro - przekroczono capacity ✗"
            else:
                message = "Wysyłka jutro - niewystarczający czas ✗"

        # Calculate confidence
        confidence = self.calculate_confidence(
            projected_utilization, time_buffer, vip_override
        )

        # Build decision factors
        factors = DecisionFactors(
            workload_impact=new_workload,
            remaining_capacity=capacity - projected_workload,
            time_buffer_minutes=time_buffer,
            bottleneck_resource=bottleneck_resource,
            congestion_factor=self.workload_calculator.calculate_congestion_factor(
                projected_utilization
            ),
            vip_override_used=vip_override,
        )

        # Create decision
        decision = Decision(
            can_ship_today=can_ship_today,
            status=status,
            confidence=confidence,
            current_utilization=projected_utilization,
            estimated_completion=estimated_completion,
            message=message,
            factors=factors,
        )

        logger.info(
            "decision_made",
            can_ship_today=can_ship_today,
            status=status.value,
            utilization=float(projected_utilization),
            confidence=float(confidence),
            priority=priority.value,
        )

        return decision


# Global service instance
_decision_engine: Optional[DecisionEngine] = None


def get_decision_engine() -> DecisionEngine:
    """Get global decision engine instance."""
    global _decision_engine
    if _decision_engine is None:
        from app.services.capacity_service import get_capacity_service
        from app.services.workload_calculator import get_workload_calculator

        _decision_engine = DecisionEngine(
            workload_calculator=get_workload_calculator(),
            capacity_service=get_capacity_service(),
        )
    return _decision_engine
