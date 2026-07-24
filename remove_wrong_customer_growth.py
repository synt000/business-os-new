from pathlib import Path

p = Path("src/services/dashboard_service.py")
s = p.read_text()

block = '''        yesterday_customers = (
            db.query(Customer)
            .filter(
                Customer.tenant_id == tenant_id,
                func.date(Customer.created_at) == yesterday
            )
            .count()
        )

        if yesterday_customers > 0:
            customer_growth = (
                (new_customers - yesterday_customers)
                / yesterday_customers
                * 100
            )
        else:
            customer_growth = 0

'''

s=s.replace(block,"")

p.write_text(s)
print("✅ removed wrong position")
