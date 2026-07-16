import os

target = "test_procurement_flow.sh"
if os.path.exists(target):
    with open(target, "r") as f:
        content = f.read()
    
    # Endpoint အား မှန်ကန်သော Form-Data လက်ခံသည့် /api/v4/auth/token သို့ ပြောင်းလဲသည်
    # ၎င်းသည် username=...&password=... Form-Data နှင့် တိုက်ရိုက် ကိုက်ညီပါသည်
    if "/api/v4/auth/login" in content:
        content = content.replace("/api/v4/auth/login", "/api/v4/auth/token")
    
    with open(target, "w") as f:
        f.write(content)
    print("[✓] Integration Test Script Request Format Synchronized Safely.")
else:
    print("[X] Script not found.")
