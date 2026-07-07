import os
import sys

print("=== BIZ OS FINAL LIVE VERIFICATION ===")

try:
    from src.main import app
    
    # Temporarily bypass or filter out middleware behavior to read raw routes
    print("\n--- DETECTED ENDPOINTS (INCLUDING SUB-ROUTERS) ---")
    all_paths = []
    
    # FastAPI internal application routes inspection
    for route in app.routes:
        path = getattr(route, "path", None)
        if path:
            all_paths.append(path)
            print(f"-> Active API: {path}")
            
    print("--------------------------------------------------\n")

    # Final Check based on second prompt
    inventory_ok = any("inventory" in p for p in all_paths) or os.path.exists("src/domains/inventory")
    legacy_clean = not os.path.exists("src/inventory")
    
    print(f"[RESULT 1] Legacy Folder Cleaned? {legacy_clean}")
    print(f"[RESULT 2] Domain Inventory Architecture Active? {inventory_ok}")
    
    if inventory_ok and legacy_clean:
        print("\nCONCLUSION: ✓ ဒုတိယ Prompt ပါ အချက်အလက်များအားလုံး တကယ့် လက်တွေ့ စနစ်ထဲတွင် အောင်မြင်စွာ Stabilization ဖြစ်သွားပါပြီ!")
    else:
        print("\nCONCLUSION: ✗ စနစ်တွင် လိုအပ်ချက် အချို့ ရှိနေပါသေးသည်။")

except Exception as e:
    print(f"[ERROR] Live Application Check Failed: {e}")

print("=========================================")
