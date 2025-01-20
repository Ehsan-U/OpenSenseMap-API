import pytest
from httpx import AsyncClient
from app import app


@pytest.fixture
async def async_client():
    """Async client fixture for integration tests."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
