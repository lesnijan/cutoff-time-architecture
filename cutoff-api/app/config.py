"""
Application configuration using pydantic-settings.
Environment variables are loaded from .env file or system environment.
"""

from functools import lru_cache
from typing import Literal

from pydantic import Field, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    app_name: str = Field(default="Cutoff Time API", description="Application name")
    version: str = Field(default="1.0.0", description="API version")
    environment: Literal["development", "staging", "production"] = Field(
        default="development", description="Environment"
    )
    debug: bool = Field(default=False, description="Debug mode")
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO", description="Log level"
    )

    # API Configuration
    api_v1_prefix: str = Field(default="/api/v1", description="API v1 prefix")
    allowed_origins: list[str] = Field(
        default_factory=lambda: ["http://localhost:3000", "http://localhost:8080"],
        description="CORS allowed origins",
    )

    # HANA Database
    hana_host: str = Field(..., description="SAP HANA host")
    hana_port: int = Field(default=30015, description="SAP HANA port")
    hana_user: str = Field(..., description="SAP HANA username")
    hana_password: str = Field(..., description="SAP HANA password")
    hana_database: str = Field(default="SYSTEMDB", description="SAP HANA database name")
    hana_encrypt: bool = Field(default=True, description="Use encrypted connection")
    hana_pool_size: int = Field(default=10, ge=1, le=50, description="Connection pool size")

    # Redis Cache
    redis_host: str = Field(default="localhost", description="Redis host")
    redis_port: int = Field(default=6379, description="Redis port")
    redis_password: str | None = Field(default=None, description="Redis password")
    redis_db: int = Field(default=0, ge=0, le=15, description="Redis database number")
    redis_ttl: int = Field(default=60, ge=10, le=300, description="Default TTL (seconds)")

    @property
    def redis_url(self) -> str:
        """Construct Redis URL."""
        if self.redis_password:
            return f"redis://:{self.redis_password}@{self.redis_host}:{self.redis_port}/{self.redis_db}"
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"

    # Rate Limiting
    rate_limit_enabled: bool = Field(default=True, description="Enable rate limiting")
    rate_limit_capacity_check: int = Field(
        default=100, ge=1, description="Rate limit for /capacity/check (per minute)"
    )
    rate_limit_cutoff: int = Field(
        default=300, ge=1, description="Rate limit for /cutoff/current (per minute)"
    )
    rate_limit_status: int = Field(
        default=60, ge=1, description="Rate limit for /status (per minute)"
    )
    rate_limit_simulate: int = Field(
        default=10, ge=1, description="Rate limit for /simulate (per minute)"
    )

    # Business Logic Configuration
    max_utilization: float = Field(
        default=0.85, ge=0.5, le=0.95, description="Maximum utilization threshold"
    )
    safety_buffer_minutes: int = Field(
        default=30, ge=15, le=60, description="Safety buffer before deadline (minutes)"
    )
    vip_reserve_percent: float = Field(
        default=0.10, ge=0.05, le=0.20, description="VIP capacity reserve (10%)"
    )
    congestion_alpha: float = Field(
        default=1.2, ge=0.5, le=2.0, description="Congestion factor alpha"
    )

    # Monitoring
    metrics_enabled: bool = Field(default=True, description="Enable Prometheus metrics")
    metrics_path: str = Field(default="/metrics", description="Metrics endpoint path")

    # Security
    jwt_secret_key: str = Field(
        default="changeme-in-production-use-strong-random-key",
        description="JWT secret key",
    )
    jwt_algorithm: str = Field(default="HS256", description="JWT algorithm")
    jwt_expiration_minutes: int = Field(
        default=60, ge=5, le=1440, description="JWT expiration (minutes)"
    )


@lru_cache
def get_settings() -> Settings:
    """
    Get cached settings instance.
    Use lru_cache to avoid re-reading environment on every call.
    """
    return Settings()  # type: ignore
