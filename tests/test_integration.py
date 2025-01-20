from fastapi.testclient import TestClient
import sys
import os

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

client = TestClient(app)


def test_version_integration():
    """Integration test for version endpoint"""
    response = client.get("/version")
    assert response.status_code == 200
    assert response.json() == {"version": "0.0.1"}


def test_temperature_integration():
    """Integration test for temperature endpoint"""
    response = client.get("/temperature")
    assert response.status_code == 200
    data = response.json()
    assert "temperature" in data
    assert isinstance(data["temperature"], float)
