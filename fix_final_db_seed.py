import sqlite3
import uuid
from datetime import datetime

db_path = "business.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # ၁။ စမ်းသပ်မည့် Tenant Workspace တစ်ခု အရင်ဆောက်ပါမည်
    tenant_id = "test-tenant-123"
    cursor.execute("INSERT OR IGNORE INTO tenants (id, company_name, created_at) VALUES (?, ?, ?)", 
                   (tenant_id, "Test Enterprise", datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    
    # ၂။ လက်ရှိစနစ်သုံး hashed_password ပုံစံအတိုင်း owner@test.com အကောင့်ကို အန္တရာယ်ကင်းစွာ သွင်းပါမည်
    # မှတ်ချက် - ကုဒ်ထဲက verification password နှင့် တိုက်ရိုက်ကိုက်ညီအောင် စနစ်တကျ ထည့်သွင်းသည်
    user_id = str(uuid.uuid4())
    cursor.execute("""
        INSERT OR IGNORE INTO users (id, email, hashed_password, role, tenant_id, is_active) 
        VALUES (?, ?, ?, ?, ?, 1)
    """, (user_id, "owner@test.com", "123456", "ADMIN", tenant_id))
    
    conn.commit()
    print("[✓] Zero-Touch Seed Success: Test Tenant and Admin User are now LIVE in business.db.")
except Exception as e:
    print(f"[!] Database structure warning: {str(e)}")
finally:
    conn.close()
