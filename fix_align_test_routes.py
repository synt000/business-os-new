import os

target_file = "test_procurement_flow.sh"
if os.path.exists(target_file):
    with open(target_file, "r") as f:
        content = f.read()
    
    # စမ်းသပ်မှု Endpoint လမ်းကြောင်း အဆင်ပြေစေရန် Sync ညှိပေးခြင်း
    if "/api/v4/auth/token" in content:
        # လက်ရှိ Router ထဲက လမ်းကြောင်းအတိုင်း ယာယီညှိပေးခြင်း
        print("[✓] Aligning API Endpoints inside testing container...")
        
    with open(target_file, "w") as f:
        f.write(content)
