from pathlib import Path

p = Path("src/domains/order/services/order_service.py")

s = p.read_text()

s = s.replace(
    ".filter(Product.id == product_id)",
    ".filter(Product.id == str(product_id))"
)

p.write_text(s)

print("ORDER SERVICE UUID FIX DONE")
