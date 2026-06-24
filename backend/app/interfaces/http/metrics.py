"""
Prometheus metrics endpoint.
"""
from fastapi import APIRouter, Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
import structlog

router = APIRouter()
logger = structlog.get_logger(__name__)


@router.get("", summary="Prometheus metrics", description="Returns Prometheus metrics in text format")
async def metrics():
    """Expose Prometheus metrics for scraping."""
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )