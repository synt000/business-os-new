import urllib.request, json
u = "http://127.0.0.1:8000"
d = {"username": "admin", "email": "admin@test.com", "password": "Admin12345", "tenant_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"}
r = urllib.request.Request(u, data=json.dumps(d).encode(), headers={"Content-Type": "application/json"})
try:
 with urllib.request.urlopen(r) as res: print("🚀 SUCCESS:", res.read().decode())
except Exception as e: print("❌ RESULT:", str(e))