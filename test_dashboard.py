from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

r = client.get("/api/v4/dashboard/summary")

print("STATUS:", r.status_code)
print("BODY:")
print(r.text)
