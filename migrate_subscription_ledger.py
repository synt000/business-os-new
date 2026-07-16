from sqlalchemy import create_engine, text

DATABASE_URL = "sqlite:///business.db"

engine = create_engine(DATABASE_URL)

with engine.begin() as conn:

    rows = conn.execute(text("""
        SELECT id, amount, reference_id, tenant_id
        FROM account_ledgers
        WHERE entry_type='INCOME'
        AND account_head='SUBSCRIPTION'
    """)).fetchall()

    count = 0

    for row in rows:

        conn.execute(text("""
            INSERT INTO account_ledgers
            (
                id,
                entry_type,
                account_head,
                amount,
                reference_id,
                description,
                created_at,
                tenant_id
            )
            VALUES
            (
                :id1,
                'DEBIT',
                'CASH_ASSET',
                :amount,
                :ref,
                'Migrated: Cash received for subscription',
                CURRENT_TIMESTAMP,
                :tenant
            )
        """), {
            "id1": "mig_debit_" + row.id,
            "amount": row.amount,
            "ref": row.reference_id,
            "tenant": row.tenant_id
        })


        conn.execute(text("""
            INSERT INTO account_ledgers
            (
                id,
                entry_type,
                account_head,
                amount,
                reference_id,
                description,
                created_at,
                tenant_id
            )
            VALUES
            (
                :id2,
                'CREDIT',
                'SUBSCRIPTION_REVENUE',
                :amount,
                :ref,
                'Migrated: Subscription revenue',
                CURRENT_TIMESTAMP,
                :tenant
            )
        """), {
            "id2": "mig_credit_" + row.id,
            "amount": row.amount,
            "ref": row.reference_id,
            "tenant": row.tenant_id
        })


        conn.execute(text("""
            DELETE FROM account_ledgers
            WHERE id=:old_id
        """), {
            "old_id": row.id
        })

        count += 1


print("Migrated:", count)
