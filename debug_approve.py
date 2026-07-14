from pathlib import Path

p = Path("src/domains/purchase/router.py")
text = p.read_text()

old = """        if product:
            product.stock_qty += item.quantity"""

new = """        if product:
            print("FOUND PRODUCT:", product.name, product.stock_qty, item.quantity)
            product.stock_qty += item.quantity
            print("NEW STOCK:", product.stock_qty)
        else:
            print("PRODUCT NOT FOUND:", item.product_id)"""

text = text.replace(old, new)

p.write_text(text)
print("Debug Added")
