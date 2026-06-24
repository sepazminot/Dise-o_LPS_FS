"""
Educational Backend - FastAPI Clean Architecture + gRPC
Main entry point for the application.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import structlog

from app.infrastructure.config.settings import get_settings
from app.infrastructure.database.session import init_db, close_db
from app.infrastructure.grpc.server import start_grpc_server, stop_grpc_server
from app.interfaces.http.health import router as health_router
from app.interfaces.http.metrics import router as metrics_router

# Configure structured logging
structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ],
    wrapper_class=structlog.make_filtering_bound_logger(20),  # INFO level
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger(__name__)
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for startup/shutdown."""
    logger.info("starting_application", environment=settings.ENVIRONMENT)
    
    # Initialize database
    await init_db()
    logger.info("database_initialized")
    
    # Start gRPC server
    grpc_task = await start_grpc_server()
    logger.info("grpc_server_started", port=settings.GRPC_PORT)
    
    yield
    
    # Shutdown
    logger.info("shutting_down_application")
    await stop_grpc_server(grpc_task)
    await close_db()
    logger.info("application_shutdown_complete")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="Educational Backend API",
        description="FastAPI Clean Architecture + gRPC for Educational Platform",
        version="0.1.0",
        docs_url="/docs" if settings.ENVIRONMENT != "production" else None,
        redoc_url="/redoc" if settings.ENVIRONMENT != "production" else None,
        openapi_url="/openapi.json" if settings.ENVIRONMENT != "production" else None,
        lifespan=lifespan,
    )
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(health_router, prefix="/health", tags=["health"])
    app.include_router(metrics_router, prefix="/metrics", tags=["metrics"])
    
    # Root endpoint
    @app.get("/", include_in_schema=False)
    async def root():
        return {
            "name": "Educational Backend",
            "version": "0.1.0",
            "environment": settings.ENVIRONMENT,
            "docs": "/docs",
            "health": "/health/live",
        }
    
    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.interfaces.main:app",
        host="0.0.0.0",
        port=settings.HTTP_PORT,
        reload=settings.ENVIRONMENT == "development",
        log_config=None,  # We use structlog
    )