from pathlib import Path

p = Path("src/services/dashboard_service.py")
s = p.read_text()

old = '''        rows = (
            db.query(
                func.date(AccountLedger.created_at),
                func.sum(AccountLedger.amount)
            )
            .filter(
                AccountLedger.tenant_id == tenant_id,
                AccountLedger.entry_type == "CREDIT",
                AccountLedger.account_head == "SALES_REVENUE"
            )
            .group_by(
                func.date(AccountLedger.created_at)
            )
            .order_by(
                func.date(AccountLedger.created_at)
            )
            .all()
        )

        return {
            "labels": [
                str(row[0])
                for row in rows
            ],
            "values": [
                float(row[1] or 0)
                for row in rows
            ],
            "revenue": [
                float(row[1] or 0)
                for row in rows
            ],
            "sales": [
                float(row[1] or 0)
                for row in rows
            ],
            "orders": []
        }
'''

new = '''        revenue_rows = (
            db.query(
                func.date(AccountLedger.created_at),
                func.sum(AccountLedger.amount)
            )
            .filter(
                AccountLedger.tenant_id == tenant_id,
                AccountLedger.entry_type == "CREDIT",
                AccountLedger.account_head == "SALES_REVENUE"
            )
            .group_by(
                func.date(AccountLedger.created_at)
            )
            .order_by(
                func.date(AccountLedger.created_at)
            )
            .all()
        )


        order_rows = (
            db.query(
                func.date(Order.created_at),
                func.count(Order.id)
            )
            .filter(
                Order.tenant_id == tenant_id
            )
            .group_by(
                func.date(Order.created_at)
            )
            .all()
        )


        order_map = {
            str(row[0]): row[1]
            for row in order_rows
        }


        return {
            "labels": [
                str(row[0])
                for row in revenue_rows
            ],

            "values": [
                float(row[1] or 0)
                for row in revenue_rows
            ],

            "revenue": [
                float(row[1] or 0)
                for row in revenue_rows
            ],

            "sales": [
                float(row[1] or 0)
                for row in revenue_rows
            ],

            "orders": [
                order_map.get(str(row[0]),0)
                for row in revenue_rows
            ]
        }
'''

if old in s:
    s=s.replace(old,new,1)
    p.write_text(s)
    print("✅ Revenue + Orders chart backend upgraded")
else:
    print("❌ chart block not found")
