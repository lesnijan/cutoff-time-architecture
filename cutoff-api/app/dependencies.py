"""
Dependency injection setup for FastAPI.
"""

from typing import AsyncGenerator

from app.core.cache import get_cache
from app.repositories.cache_repository import get_cache_repository
from app.repositories.hana_repository import get_hana_repository
from app.services.capacity_service import get_capacity_service
from app.services.decision_engine import get_decision_engine
from app.services.workload_calculator import get_workload_calculator


# Dependency factories for repositories
async def get_hana_dependency() -> AsyncGenerator:
    """Get HANA repository with lifecycle management."""
    repo = get_hana_repository()
    try:
        await repo.connect()
        yield repo
    finally:
        await repo.disconnect()


async def get_cache_dependency() -> AsyncGenerator:
    """Get cache client with lifecycle management."""
    cache = get_cache()
    try:
        await cache.connect()
        yield cache
    finally:
        await cache.disconnect()


# Service dependencies
def get_workload_calculator_dependency():
    """Get workload calculator service."""
    return get_workload_calculator()


def get_capacity_service_dependency():
    """Get capacity service."""
    return get_capacity_service()


def get_decision_engine_dependency():
    """Get decision engine."""
    return get_decision_engine()


def get_cache_repository_dependency():
    """Get cache repository."""
    return get_cache_repository()
