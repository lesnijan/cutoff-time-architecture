"""
Redis cache client and utilities.
"""

import hashlib
import json
from typing import Any, Optional

import redis.asyncio as aioredis
from redis.asyncio import Redis

from app.config import get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class CacheClient:
    """Redis cache client with utility methods."""

    def __init__(self) -> None:
        """Initialize cache client."""
        self._redis: Optional[Redis] = None
        self._settings = get_settings()

    async def connect(self) -> None:
        """Connect to Redis."""
        try:
            self._redis = await aioredis.from_url(
                self._settings.redis_url,
                encoding="utf-8",
                decode_responses=True,
            )
            await self._redis.ping()
            logger.info("redis_connected", host=self._settings.redis_host)
        except Exception as e:
            logger.error("redis_connection_failed", error=str(e))
            raise

    async def disconnect(self) -> None:
        """Disconnect from Redis."""
        if self._redis:
            await self._redis.close()
            logger.info("redis_disconnected")

    @property
    def redis(self) -> Redis:
        """Get Redis client instance."""
        if self._redis is None:
            raise RuntimeError("Redis client not connected. Call connect() first.")
        return self._redis

    def generate_key(self, prefix: str, **kwargs: Any) -> str:
        """
        Generate cache key from prefix and parameters.

        Args:
            prefix: Key prefix (e.g., 'capacity', 'cutoff')
            **kwargs: Parameters to include in key

        Returns:
            Cache key string
        """
        # Sort kwargs for consistent key generation
        sorted_params = sorted(kwargs.items())
        param_str = json.dumps(sorted_params, sort_keys=True)
        param_hash = hashlib.md5(param_str.encode()).hexdigest()[:8]
        return f"{prefix}:{param_hash}"

    async def get(self, key: str) -> Optional[str]:
        """
        Get value from cache.

        Args:
            key: Cache key

        Returns:
            Cached value or None if not found
        """
        try:
            value = await self.redis.get(key)
            if value:
                logger.debug("cache_hit", key=key)
            else:
                logger.debug("cache_miss", key=key)
            return value
        except Exception as e:
            logger.error("cache_get_error", key=key, error=str(e))
            return None

    async def set(
        self, key: str, value: str, ttl: Optional[int] = None
    ) -> bool:
        """
        Set value in cache with optional TTL.

        Args:
            key: Cache key
            value: Value to cache
            ttl: Time-to-live in seconds (defaults to settings.redis_ttl)

        Returns:
            True if successful
        """
        try:
            ttl = ttl or self._settings.redis_ttl
            await self.redis.set(key, value, ex=ttl)
            logger.debug("cache_set", key=key, ttl=ttl)
            return True
        except Exception as e:
            logger.error("cache_set_error", key=key, error=str(e))
            return False

    async def delete(self, key: str) -> bool:
        """
        Delete key from cache.

        Args:
            key: Cache key

        Returns:
            True if key was deleted
        """
        try:
            result = await self.redis.delete(key)
            logger.debug("cache_delete", key=key, deleted=bool(result))
            return bool(result)
        except Exception as e:
            logger.error("cache_delete_error", key=key, error=str(e))
            return False

    async def increment(self, key: str, amount: int = 1) -> int:
        """
        Increment counter.

        Args:
            key: Counter key
            amount: Amount to increment

        Returns:
            New counter value
        """
        try:
            value = await self.redis.incrby(key, amount)
            return int(value)
        except Exception as e:
            logger.error("cache_increment_error", key=key, error=str(e))
            return 0

    async def expire(self, key: str, ttl: int) -> bool:
        """
        Set TTL on existing key.

        Args:
            key: Cache key
            ttl: Time-to-live in seconds

        Returns:
            True if successful
        """
        try:
            result = await self.redis.expire(key, ttl)
            return bool(result)
        except Exception as e:
            logger.error("cache_expire_error", key=key, error=str(e))
            return False


# Global cache instance
_cache_client: Optional[CacheClient] = None


def get_cache() -> CacheClient:
    """Get global cache client instance."""
    global _cache_client
    if _cache_client is None:
        _cache_client = CacheClient()
    return _cache_client
