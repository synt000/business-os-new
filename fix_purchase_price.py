from pathlib import Path

p = Path("src/domains/ai_insight/service.py")

text = p.read_text(encoding="utf-8")

old = """unit_cost = (
        product.cost_price
        if hasattr(product, "cost_price")
        else 0
    )"""

new = """unit_cost = product.purchase_price or 0"""

if old in text:
    text = text.replace(old, new)
    p.write_text(text, encoding="utf-8")
    print("✅ purchase_price Fix Applied")
else:
    print("⚠️ Old cost_price block not found")
