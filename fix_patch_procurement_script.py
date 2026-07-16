import os

target = "test_procurement_flow.sh"
if os.path.exists(target):
    with open(target, "r") as f:
        content = f.read()
    
    # /api/v4/auth/token လမ်းကြောင်းအား ပင်မအလုပ်လုပ်သော auth/token သို့ တိုက်ရိုက် sync ညှိပေးခြင်း
    if "/api/v4/auth/token" in content:
        content = content.replace("/api/v4/auth/token", "/api/v4/auth/login")
        with open(target, "w") as f:
            f.write(content)
        print("[✓] Procurement Script API Endpoint Synchronized Successfully.")
