from sqlalchemy import text
from src.core.database import engine
import json

with engine.connect() as conn:

    customer = conn.execute(
        text("""
            SELECT id, customer_name
            FROM customers
            LIMIT 1
        """)
    ).fetchone()

    product = conn.execute(
        text("""
            SELECT id, name
            FROM products
            LIMIT 1
        """)
    ).fetchone()

    if not customer:
        raise SystemExit("NO CUSTOMER FOUND")

    if not product:
        raise SystemExit("NO PRODUCT FOUND")

    payload = {
        "customer_id": str(customer.id),
        "platform_channel": "SYSTEM",
        "items": [
            {
                "product_id": str(product.id),
                "quantity": 1
            }
        ]
    }

    with open("order_test.json", "w") as f:
        json.dump(payload, f, indent=2)

    print("ORDER TEST PAYLOAD CREATED")
    print(json.dumps(payload, indent=2))

