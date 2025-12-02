"""
Cache repository for storing and retrieving cached capacity decisions.
"""

import json
from datetime import datetime
from decimal import Decimal
from typing import Any, Optional

from app.core.cache import get_cache
from app.core.logging import get_logger
from app.models.domain import Decision
from app.models.requests import CapacityCheckRequest

logger = get_logger(__name__)


class CacheRepository:
    """Repository for cache operations."""

    def __init__(self) -> None:
        """Initialize cache repository."""
        self._cache = get_cache()

    def _serialize_decision(self, decision: Decision) -> str:
        """
        Serialize Decision object to JSON string.

        Args:
            decision: Decision object

        Returns:
            JSON string
        """
        # Convert to dict and handle Decimal/datetime serialization
        data = decision.model_dump(mode="json")
        return json.dumps(data, default=str)

    def _deserialize_decision(self, data: str) -> Decision:
        """
        Deserialize JSON string to Decision object.

        Args:
            data: JSON string

        Returns:
            Decision object
        """
        parsed = json.loads(data)
        return Decision(**parsed)

    async def get_cached_decision(
        self, request: CapacityCheckRequest
    ) -> Optional[Decision]:
        """
        Get cached decision for a capacity check request.

        Args:
            request: Capacity check request

        Returns:
            Cached Decision or None
        """
        # Generate cache key from request parameters
        key = self._cache.generate_key(
            "capacity",
            warehouse_id=request.warehouse_id,
            priority=request.priority.value,
            items=[(item.product_id, item.quantity) for item in request.items],
        )

        cached_data = await self._cache.get(key)
        if cached_data:
            try:
                decision = self._deserialize_decision(cached_data)
                logger.info("cache_decision_hit", key=key)
                return decision
            except Exception as e:
                logger.error("cache_deserialize_error", key=key, error=str(e))
                return None

        logger.debug("cache_decision_miss", key=key)
        return None

    async def cache_decision(
        self, request: CapacityCheckRequest, decision: Decision, ttl: Optional[int] = None
    ) -> bool:
        """
        Cache a capacity decision.

        Args:
            request: Capacity check request
            decision: Decision to cache
            ttl: Time-to-live in seconds

        Returns:
            True if successful
        """
        key = self._cache.generate_key(
            "capacity",
            warehouse_id=request.warehouse_id,
            priority=request.priority.value,
            items=[(item.product_id, item.quantity) for item in request.items],
        )

        try:
            serialized = self._serialize_decision(decision)
            result = await self._cache.set(key, serialized, ttl)
            if result:
                logger.info("cache_decision_stored", key=key, ttl=ttl)
            return result
        except Exception as e:
            logger.error("cache_store_error", key=key, error=str(e))
            return False

    async def invalidate_warehouse_cache(self, warehouse_id: str) -> int:
        """
        Invalidate all cache entries for a warehouse.

        Args:
            warehouse_id: Warehouse identifier

        Returns:
            Number of keys deleted
        """
        # TODO: Implement pattern-based deletion
        # This requires SCAN command in Redis
        logger.info("cache_invalidate_warehouse", warehouse_id=warehouse_id)
        return 0

    async def increment_rate_limit(
        self, user_id: str, endpoint: str, window_seconds: int = 60
    ) -> int:
        """
        Increment rate limit counter for user and endpoint.

        Args:
            user_id: User identifier
            endpoint: API endpoint
            window_seconds: Rate limit window in seconds

        Returns:
            Current count
        """
        key = f"ratelimit:{user_id}:{endpoint}"
        count = await self._cache.increment(key)

        # Set TTL only on first increment
        if count == 1:
            await self._cache.expire(key, window_seconds)

        return count

    async def get_rate_limit_count(self, user_id: str, endpoint: str) -> int:
        """
        Get current rate limit count for user and endpoint.

        Args:
            user_id: User identifier
            endpoint: API endpoint

        Returns:
            Current count
        """
        key = f"ratelimit:{user_id}:{endpoint}"
        value = await self._cache.get(key)
        return int(value) if value else 0


# Global repository instance
_cache_repository: Optional[CacheRepository] = None


def get_cache_repository() -> CacheRepository:
    """Get global cache repository instance."""
    global _cache_repository
    if _cache_repository is None:
        _cache_repository = CacheRepository()
    return _cache_repository
