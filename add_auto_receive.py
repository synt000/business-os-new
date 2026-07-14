from pathlib import Path

p = Path("src/domains/purchase/router.py")
text = p.read_text(encoding="utf-8")

if "PurchaseItem" in text and "product.stock_qty +=" in text:
    print("Already patched")
    raise SystemExit

text = text.replace(
"from src.models.saas_core import User, PurchaseOrder",
"""from src.models.saas_core import (
    User,
    PurchaseOrder,
    PurchaseItem,
    Product,
)"""
)

old = """    po.status = "APPROVED"

    db.commit()

    return {
        "status":"SUCCESS",
        "message":"Purchase Order Approved",
        "purchase_number":po.purchase_number
    }"""

new = """    po.status = "APPROVED"

    items = (
        db.query(PurchaseItem)
        .filter(
            PurchaseItem.purchase_order_id == po.id
        )
        .all()
    )

    for item in items:

        product = (
            db.query(Product)
            .filter(Product.id == item.product_id)
            .first()
        )

        if product:
            product.stock_qty += item.quantity

    db.commit()

    return {
        "status":"SUCCESS",
        "message":"Purchase Order Approved & Stock Received",
        "purchase_number":po.purchase_number
    }"""

text = text.replace(old, new)

p.write_text(text, encoding="utf-8")

print("Auto Stock Receive Added")
