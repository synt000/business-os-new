import sqlite3

db_path = "business.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    print("=== INITIALIZING SUBSCRIPTION & PAYMENT SYSTEM SCHEMAS ===")
    
    # ၁။ Tenant Subscriptions Table (လုပ်ငန်းတစ်ခုချင်းစီရဲ့ သက်တမ်းကုန်ဆုံးမည့် ရက်စွဲနှင့် Plan ကို ထိန်းသိမ်းရန်)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tenant_subscriptions (
        id TEXT PRIMARY KEY,
        tenant_id TEXT NOT NULL,
        current_plan TEXT DEFAULT 'FREE_TRIAL', -- FREE_TRIAL, STANDARD_MONTHLY, ENTERPRISE
        trial_start_date TEXT,
        trial_end_date TEXT,
        subscription_status TEXT DEFAULT 'ACTIVE', -- ACTIVE, EXPIRED, PAST_DUE
        last_payment_date TEXT,
        next_billing_date TEXT
    );
    """)
    print("[✓] Table 'tenant_subscriptions' verified/created.")

    # ၂။ SaaS Gateway Payments Table (လုပ်ငန်းရှင်များက စနစ်ငှားရမ်းခပေးချေသည့် အဝယ်စာရင်းမှတ်တမ်း)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS saas_gateway_payments (
        id TEXT PRIMARY KEY,
        tenant_id TEXT NOT NULL,
        invoice_number TEXT NOT NULL,
        amount_paid REAL DEFAULT 0.0,
        payment_method TEXT, -- KBZ_PAY, WAVE_PAY, BANK_TRANSFER
        transaction_reference TEXT,
        payment_status TEXT DEFAULT 'COMPLETED', -- PENDING, COMPLETED, FAILED
        paid_at TEXT DEFAULT CURRENT_TIMESTAMP
    );
    """)
    print("[✓] Table 'saas_gateway_payments' verified/created.")

    conn.commit()
    print("\n[✓] SCHEMA DEPLOYMENT SUCCESS: Subscription & Payment System Tables are now ready in business.db.")
except Exception as e:
    print(f"[X] Schema creation failed: {str(e)}")
finally:
    conn.close()
