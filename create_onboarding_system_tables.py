import sqlite3

db_path = "business.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    print("=== INITIALIZING CUSTOMER ONBOARDING & TENANT REGISTRATION SCHEMAS ===")
    
    # ၁။ Tenant Registrations Table (လုပ်ငန်းအသစ်များ လျှောက်ထားမှု စာရင်းကို ထိန်းသိမ်းရန်)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tenant_registrations (
        id TEXT PRIMARY KEY,
        business_name TEXT NOT NULL,
        owner_email TEXT NOT NULL,
        phone_number TEXT,
        plan_selected TEXT DEFAULT 'FREE_TRIAL', -- FREE_TRIAL, STANDARD, ENTERPRISE
        onboarding_status TEXT DEFAULT 'PENDING', -- PENDING, APPROVED, REJECTED
        registered_at TEXT DEFAULT CURRENT_TIMESTAMP
    );
    """)
    print("[✓] Table 'tenant_registrations' verified/created.")

    # ၂။ Onboarding Workflows Table (လုပ်ငန်းတစ်ခုချင်းစီ Onboarding Step ဘယ်နားရောက်နေလဲ ခြေရာခံရန်)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS onboarding_workflows (
        id TEXT PRIMARY KEY,
        tenant_id TEXT NOT NULL,
        step_1_profile_completed INTEGER DEFAULT 0, -- 0 = No, 1 = Yes
        step_2_inventory_initialized INTEGER DEFAULT 0,
        step_3_payment_configured INTEGER DEFAULT 0,
        current_step TEXT DEFAULT 'PROFILE_SETUP', -- PROFILE_SETUP, INVENTORY_SETUP, READY
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP
    );
    """)
    print("[✓] Table 'onboarding_workflows' verified/created.")

    conn.commit()
    print("\n[✓] SCHEMA DEPLOYMENT SUCCESS: Onboarding System Tables are now LIVE in business.db.")
except Exception as e:
    print(f"[X] Schema creation failed: {str(e)}")
finally:
    conn.close()
