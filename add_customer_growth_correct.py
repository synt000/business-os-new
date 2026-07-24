from pathlib import Path

p = Path("src/services/dashboard_service.py")
s=p.read_text()

old = '''        yesterday_orders = ('''

new = '''        yesterday_customers = (
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


        yesterday_orders = ('''

if old in s:
    s=s.replace(old,new,1)

p.write_text(s)
print("✅ customer growth moved correctly")
