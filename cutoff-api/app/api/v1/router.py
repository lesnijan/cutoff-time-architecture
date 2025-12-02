"""
API v1 router - aggregates all endpoint routers.
"""

from fastapi import APIRouter

from app.api.v1.endpoints import capacity, cutoff, demo, health, simulate, status

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(health.router, tags=["Health"])
api_router.include_router(capacity.router, tags=["Capacity"])
api_router.include_router(cutoff.router, tags=["Cutoff"])
api_router.include_router(status.router, tags=["Status"])
api_router.include_router(simulate.router, tags=["Simulation"])
api_router.include_router(demo.router, tags=["Demo"])
