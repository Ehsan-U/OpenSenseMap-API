# write tests for the app
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_get_version():
    response = client.get("/version")
    assert response.status_code == 200
    assert response.json() == {"version": "0.0.1"}
