from pathlib import Path

path = Path("src/product/router.py")

text = path.read_text()

duplicate = '''    invoice = db.query(Invoice).filter(
        Invoice.order_id == order.id,
        Invoice.tenant_id == current_user.tenant_id
    ).first()

'''

first = text.find(duplicate)

second = text.find(duplicate, first + 1)

if second == -1:
    raise SystemExit("SECOND BLOCK NOT FOUND")

text = text[:second] + text[second + len(duplicate):]

path.write_text(text)

print("REMOVED DUPLICATE INVOICE QUERY")
