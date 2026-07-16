import sqlite3

db_path = "business.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    print("=== INITIALIZING BUSINESS RENTAL SYSTEM SCHEMAS ===")
    
    # ၁။ Rental Items Table (ငှားရမ်းမည့် ကား၊ ကုန်ပစ္စည်း သို့မဟုတ် အခန်း/နေရာများ စီမံရန်)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rental_items (
        id TEXT PRIMARY KEY,
        tenant_id TEXT NOT NULL,
        item_name TEXT NOT NULL,
        category TEXT,
        rate_per_hour REAL DEFAULT 0.0,
        rate_per_day REAL DEFAULT 0.0,
        status TEXT DEFAULT 'AVAILABLE', -- AVAILABLE, RENTED, MAINTENANCE
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    );
    """)
    print("[✓] Table 'rental_items' verified/created.")

    # ၂။ Rentals Table (ဘယ်သူက၊ ဘာကို၊ ဘယ်နှစ်ရက် ငှားရမ်းသွားတယ်ဆိုတဲ့ အဓိက စာရင်း)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rentals (
        id TEXT PRIMARY KEY,
        tenant_id TEXT NOT NULL,
        customer_id TEXT,
        item_id TEXT NOT NULL,
        start_time TEXT NOT NULL,
        end_time TEXT NOT NULL,
        total_amount REAL DEFAULT 0.0,
        rental_status TEXT DEFAULT 'PENDING', -- PENDING, ACTIVE, COMPLETED, CANCELLED
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (item_id) REFERENCES rental_items(id)
    );
    """)
    print("[✓] Table 'rentals' verified/created.")

    # ၃။ Rental Payments Table (ငှားရမ်းမှုအတွက် ငွေဝင်စာရင်း စစ်ဆေးရန်)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rental_payments (
        id TEXT PRIMARY KEY,
        tenant_id TEXT NOT NULL,
        rental_id TEXT NOT NULL,
        amount_paid REAL DEFAULT 0.0,
        payment_method TEXT, -- CASH, KBZ_PAY, WAVE, CARD
        payment_status TEXT DEFAULT 'PAID',
        paid_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (rental_id) REFERENCES rentals(id)
    );
    """)
    print("[✓] Table 'rental_payments' verified/created.")

    conn.commit()
    print("\n[✓] SCHEMA DEPLOYMENT SUCCESS: Rental System Tables are now ready in business.db.")
except Exception as e:
    print(f"[X] Schema creation failed: {str(e)}")
finally:
    conn.close()
