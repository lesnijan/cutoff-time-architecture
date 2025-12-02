"""
Demo endpoints for scenario management.
"""

from fastapi import APIRouter
from pydantic import BaseModel

from app.core.logging import get_logger
from app.repositories.mock_hana_data import DEMO_SCENARIOS, set_demo_scenario

router = APIRouter()
logger = get_logger(__name__)


class ScenarioInfo(BaseModel):
    """Scenario information."""

    name: str
    description: str
    utilization: float
    status: str


class ScenariosResponse(BaseModel):
    """Available demo scenarios."""

    scenarios: dict[str, ScenarioInfo]
    current: str


@router.get(
    "/demo/scenarios",
    response_model=ScenariosResponse,
    summary="Get available demo scenarios",
    description="List all available demo scenarios for testing different warehouse states.",
    tags=["Demo"],
)
async def get_demo_scenarios() -> ScenariosResponse:
    """Get list of available demo scenarios."""
    scenarios = {}

    for key, scenario in DEMO_SCENARIOS.items():
        scenarios[key] = ScenarioInfo(
            name=scenario["name"],
            description=scenario["description"],
            utilization=float(scenario["utilization"]),
            status=scenario["status"].value,
        )

    logger.info("demo_scenarios_listed", count=len(scenarios))

    return ScenariosResponse(
        scenarios=scenarios,
        current="normal",  # TODO: Track current scenario
    )


@router.post(
    "/demo/scenario/{scenario_name}",
    summary="Switch demo scenario",
    description="Switch to a different demo scenario to test various warehouse states.",
    tags=["Demo"],
)
async def set_scenario(scenario_name: str) -> dict:
    """
    Switch to a different demo scenario.

    Args:
        scenario_name: Scenario to switch to (normal, low, high, overload)

    Returns:
        Success message with new scenario info
    """
    if scenario_name not in DEMO_SCENARIOS:
        return {
            "success": False,
            "message": f"Unknown scenario: {scenario_name}",
            "available": list(DEMO_SCENARIOS.keys()),
        }

    set_demo_scenario(scenario_name)
    scenario = DEMO_SCENARIOS[scenario_name]

    logger.info("demo_scenario_changed", scenario=scenario_name)

    return {
        "success": True,
        "message": f"Switched to scenario: {scenario['name']}",
        "scenario": {
            "name": scenario["name"],
            "description": scenario["description"],
            "utilization": float(scenario["utilization"]),
            "status": scenario["status"].value,
        },
    }
