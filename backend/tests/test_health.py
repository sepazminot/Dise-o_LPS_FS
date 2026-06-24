"""
Backend Tests - Unit tests for health endpoints
"""
import pytest
from httpx import AsyncClient, ASGITransport
from app.interfaces.main import create_app


@pytest.fixture
async def async_client():
    """Create async test client."""
    app = create_app()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


class TestHealthEndpoints:
    """Test health check endpoints."""

    @pytest.mark.asyncio
    async def test_liveness(self, async_client):
        """Test liveness probe."""
        response = await async_client.get("/health/live")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "alive"
        assert data["service"] == "educational-backend"

    @pytest.mark.asyncio
    async def test_startup(self, async_client):
        """Test startup probe."""
        response = await async_client.get("/health/startup")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "started"
        assert data["service"] == "educational-backend"

    @pytest.mark.asyncio
    async def test_readiness_without_db(self, async_client):
        """Test readiness probe fails without DB."""
        # This will fail because DB is not available in test
        # In real tests, use testcontainers for real DB
        response = await async_client.get("/health/ready")
        assert response.status_code == 503


class TestRootEndpoint:
    """Test root endpoint."""

    @pytest.mark.asyncio
    async def test_root(self, async_client):
        """Test root endpoint returns basic info."""
        response = await async_client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Educational Backend"
        assert "version" in data
        assert "environment" in data