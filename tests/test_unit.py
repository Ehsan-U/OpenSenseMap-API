from fastapi.testclient import TestClient
import pytest
from httpx import AsyncClient
import sys
import os
from unittest.mock import AsyncMock

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

client = TestClient(app)


def test_get_version():
    """Unit test for version endpoint"""
    response = client.get("/version")
    assert response.status_code == 200
    assert response.json() == {"version": "0.0.1"}


@pytest.mark.asyncio(loop_scope="function")
async def test_get_temperature_success():
    """Unit test for temperature endpoint - successful case"""
    async with AsyncClient(base_url="http://test") as ac:
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"temperature": 20.5}

        ac.get = AsyncMock(return_value=mock_response)
        response = await ac.get("/temperature")

        assert response.status_code == 200
        response_data = await response.json()
        assert response_data == {"temperature": 20.5}


@pytest.mark.asyncio(loop_scope="function")
async def test_get_temperature_no_data():
    """Unit test for temperature endpoint - no sensor data"""
    async with AsyncClient(base_url="http://test") as ac:
        mock_response = AsyncMock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"detail": "No temperature sensors found"}

        ac.get = AsyncMock(return_value=mock_response)
        response = await ac.get("/temperature")

        assert response.status_code == 404


@pytest.mark.asyncio(loop_scope="function")
async def test_get_temperature_api_error():
    """Unit test for temperature endpoint - API error"""
    async with AsyncClient(base_url="http://test") as ac:
        mock_response = AsyncMock()
        mock_response.status_code = 500
        mock_response.json.side_effect = Exception("API Error")

        ac.get = AsyncMock(return_value=mock_response)
        response = await ac.get("/temperature")

        assert response.status_code == 500
