"""
Prometheus metrics configuration and collectors.
"""

from prometheus_client import Counter, Gauge, Histogram, Info

# API Request Metrics
http_requests_total = Counter(
    "cutoff_api_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"],
)

http_request_duration_seconds = Histogram(
    "cutoff_api_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "endpoint"],
    buckets=(0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0),
)

# Business Metrics
capacity_checks_total = Counter(
    "cutoff_capacity_checks_total",
    "Total capacity check requests",
    ["decision", "priority"],
)

warehouse_utilization = Gauge(
    "cutoff_warehouse_utilization",
    "Current warehouse utilization (0-1)",
    ["warehouse_id"],
)

warehouse_capacity = Gauge(
    "cutoff_warehouse_capacity",
    "Current warehouse capacity in units",
    ["warehouse_id", "resource_type"],
)

orders_in_queue = Gauge(
    "cutoff_orders_in_queue",
    "Number of orders currently in queue",
    ["warehouse_id", "status"],
)

cutoff_time_remaining_minutes = Gauge(
    "cutoff_time_remaining_minutes",
    "Minutes remaining until cutoff",
    ["warehouse_id"],
)

# Cache Metrics
cache_hits_total = Counter(
    "cutoff_cache_hits_total",
    "Total cache hits",
    ["cache_type"],
)

cache_misses_total = Counter(
    "cutoff_cache_misses_total",
    "Total cache misses",
    ["cache_type"],
)

# Database Metrics
db_query_duration_seconds = Histogram(
    "cutoff_db_query_duration_seconds",
    "Database query duration in seconds",
    ["query_type"],
    buckets=(0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5),
)

db_connection_pool_size = Gauge(
    "cutoff_db_connection_pool_size",
    "Database connection pool size",
    ["pool_name"],
)

# Application Info
app_info = Info(
    "cutoff_api_info",
    "Application information",
)


def initialize_metrics(app_name: str, version: str, environment: str) -> None:
    """
    Initialize application info metrics.

    Args:
        app_name: Application name
        version: Application version
        environment: Environment (dev/staging/prod)
    """
    app_info.info({
        "app_name": app_name,
        "version": version,
        "environment": environment,
    })
