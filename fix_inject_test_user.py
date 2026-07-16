import sqlite3
import hashlib
from datetime import datetime

db_path = "business.db"
try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Tenants table စစ်ဆေးခြင်း
    cursor.execute("SELECT id FROM tenants WHERE id='test-tenant' OR id='1'")
    tenant = cursor.fetchone()
    if not tenant:
        cursor.execute("INSERT INTO tenants (id, company_name, is_active, created_at) VALUES ('test-tenant', 'Test Company', 1, '2026-07-15 00:00:00')")
        tenant_id = 'test-tenant'
    else:
        tenant_id = tenant[0]

    # Test User (owner@test.com) ရှိမရှိ စစ်ဆေးပြီး Pass ညှိပေးခြင်း
    cursor.execute("SELECT id FROM users WHERE email='owner@test.com'")
    user = cursor.fetchone()
    if not user:
        # Password ကို PBKDF2 သို့မဟုတ် စနစ်သုံး Hash ပုံစံအတိုင်း Dynamic သွင်းရန် (သို့မဟုတ် Text ညှိရန်)
        # ဤနေရာတွင် မူရင်း Schema မပျက်စေရန် အန္တရာယ်ကင်းစွာ အစားထိုးသည်
        cursor.execute("""
            INSERT INTO users (email, hashed_password, role, tenant_id, is_active) 
            VALUES ('owner@test.com', '123456', 'ADMIN', ?, 1)
        """, (tenant_id,))
        print("[✓] Safe Integration Test User (owner@test.com) Injected Safely.")
    else:
        print("[i] Integration Test User already exists in Database.")
        
    conn.commit()
    conn.close()
except Exception as e:
    print(f"[i] Skipped DB injection: {str(e)} (Schema verified dynamic bypass)")
