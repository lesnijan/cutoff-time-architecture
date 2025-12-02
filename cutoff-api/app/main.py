"""
Main FastAPI application entry point.
"""

import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from prometheus_client import make_asgi_app

from app.api.v1.router import api_router
from app.config import get_settings
from app.core.cache import get_cache
from app.core.logging import configure_logging, get_logger
from app.core.metrics import http_request_duration_seconds, http_requests_total, initialize_metrics
from app.repositories.hana_repository import get_hana_repository

# Configure logging first
configure_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan events.
    Handles startup and shutdown tasks.
    """
    settings = get_settings()

    # Startup
    logger.info(
        "application_starting",
        app_name=settings.app_name,
        version=settings.version,
        environment=settings.environment,
    )

    # Initialize metrics
    initialize_metrics(settings.app_name, settings.version, settings.environment)

    # Connect to services
    try:
        cache = get_cache()
        await cache.connect()
        logger.info("cache_connected")
    except Exception as e:
        logger.warning("cache_connection_failed", error=str(e))

    try:
        hana = get_hana_repository()
        await hana.connect()
        logger.info("hana_connected")
    except Exception as e:
        logger.warning("hana_connection_failed", error=str(e))

    logger.info("application_started")

    yield

    # Shutdown
    logger.info("application_shutting_down")

    try:
        cache = get_cache()
        await cache.disconnect()
        logger.info("cache_disconnected")
    except Exception:
        pass

    try:
        hana = get_hana_repository()
        await hana.disconnect()
        logger.info("hana_disconnected")
    except Exception:
        pass

    logger.info("application_stopped")


# Create FastAPI app
settings = get_settings()
app = FastAPI(
    title=settings.app_name,
    description="Dynamic warehouse capacity and cutoff time calculation API",
    version=settings.version,
    docs_url=f"{settings.api_v1_prefix}/docs",
    redoc_url=f"{settings.api_v1_prefix}/redoc",
    openapi_url=f"{settings.api_v1_prefix}/openapi.json",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add timing and logging for all requests."""
    start_time = time.time()

    # Process request
    try:
        response = await call_next(request)
        process_time = time.time() - start_time

        # Add timing header
        response.headers["X-Process-Time"] = str(process_time)

        # Record metrics
        http_requests_total.labels(
            method=request.method,
            endpoint=request.url.path,
            status=response.status_code,
        ).inc()

        http_request_duration_seconds.labels(
            method=request.method,
            endpoint=request.url.path,
        ).observe(process_time)

        # Log request
        logger.info(
            "request_completed",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration_seconds=process_time,
        )

        return response

    except Exception as e:
        process_time = time.time() - start_time

        logger.error(
            "request_failed",
            method=request.method,
            path=request.url.path,
            error=str(e),
            duration_seconds=process_time,
        )

        # Record error metric
        http_requests_total.labels(
            method=request.method,
            endpoint=request.url.path,
            status=500,
        ).inc()

        return JSONResponse(
            status_code=500,
            content={
                "error": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred",
            },
        )


# Include API router
app.include_router(api_router, prefix=settings.api_v1_prefix)

# Mount static files for demo
app.mount("/static", StaticFiles(directory="static"), name="static")

# Mount Prometheus metrics endpoint
if settings.metrics_enabled:
    metrics_app = make_asgi_app()
    app.mount(settings.metrics_path, metrics_app)


@app.get("/", include_in_schema=False)
async def root():
    """Root endpoint - redirect to demo."""
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.version,
        "demo": "/static/demo.html",
        "docs": f"{settings.api_v1_prefix}/docs",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8080,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )
