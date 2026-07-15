from pathlib import Path

p = Path("src/domains/order/services/order_service.py")
text = p.read_text()

old = """)
    ).first()"""

# remove broken empty chain pattern
text = text.replace(
"""    product = (
    ).first()""",
"""    product = (
        db.query(Product)
        .filter(Product.id == item.product_id)
        .first()
    )"""
)

p.write_text(text)
print("order_service fixed check ✅")
