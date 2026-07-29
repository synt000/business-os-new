from fastapi.testclient import TestClient
from apps.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "ok"
    assert data["service"] == "business-os"
    assert data["version"] == "5.5.0-Enterprise"
