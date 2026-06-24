"""
Health check endpoints for Kubernetes probes.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
import redis.asyncio as redis
import structlog

from app.infrastructure.database.session import get_db
from app.infrastructure.config.settings import get_settings

router = APIRouter()
logger = structlog.get_logger(__name__)
settings = get_settings()


@router.get("/live", summary="Liveness probe", description="Kubernetes liveness probe - checks if process is alive")
async def liveness():
    """Liveness probe - returns 200 if process is running."""
    return {"status": "alive", "service": "educational-backend"}


@router.get("/ready", summary="Readiness probe", description="Kubernetes readiness probe - checks if service can handle requests")
async def readiness(db: AsyncSession = Depends(get_db)):
    """Readiness probe - checks DB and Redis connectivity."""
    checks = {}
    
    # Check database
    try:
        await db.execute(text("SELECT 1"))
        checks["database"] = "ok"
    except Exception as e:
        logger.error("readiness_db_check_failed", error=str(e))
        checks["database"] = "failed"
    
    # Check Redis
    try:
        redis_client = redis.from_url(settings.REDIS_URL)
        await redis_client.ping()
        await redis_client.close()
        checks["redis"] = "ok"
    except Exception as e:
        logger.error("readiness_redis_check_failed", error=str(e))
        checks["redis"] = "failed"
    
    # Determine overall status
    all_ok = all(v == "ok" for v in checks.values())
    
    if not all_ok:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"status": "not_ready", "checks": checks}
        )
    
    return {"status": "ready", "checks": checks}


@router.get("/startup", summary="Startup probe", description="Kubernetes startup probe - checks if application has started")
async def startup():
    """Startup probe - returns 200 once application is fully initialized."""
    # Could check for completed migrations, cache warmup, etc.
    return {"status": "started", "service": "educational-backend"}