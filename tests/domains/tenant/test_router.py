from fastapi.testclient import TestClient
from apps.main import app 

client = TestClient(app)

def test_post_tenant_201():
    # ဒီ test က main.py မှာ router မထည့်ရသေးလို့ 404 တက်ရမယ် (ဒါမှ Red Phase ဖြစ်မယ်)
    response = client.post("/api/v1/tenants/", json={"name": "New Biz", "slug": "new-biz"})
    assert response.status_code == 201
