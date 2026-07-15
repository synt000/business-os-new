from pathlib import Path

p = Path("src/domains/order/services/order_service.py")
text = p.read_text()

old = """    inventory_cost = sum(
        (
            .first()
            .purchase_price
        ) * item.quantity
        for item in items
    )"""

new = """    inventory_cost = 0

    for item in items:
        product_id = item['product_id'] if isinstance(item, dict) else item.product_id

        product = (
            db.query(Product)
            .filter(Product.id == product_id)
            .first()
        )

        if product:
            qty = item['quantity'] if isinstance(item, dict) else item.quantity
            inventory_cost += product.purchase_price * qty"""

if old in text:
    text = text.replace(old, new)
    p.write_text(text)
    print("Inventory cost query fixed ✅")
else:
    print("Target not found ❌")
