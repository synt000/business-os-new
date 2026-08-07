from pathlib import Path

p = Path("src/main.py")
s = p.read_text()

old = "app.include_router(supplier_payment_router)"

new = old + "\napp.include_router(customer_payment_router)"

if "app.include_router(customer_payment_router)" not in s:
    s = s.replace(old, new)
    p.write_text(s)
    print("INCLUDE ADDED")
else:
    print("ALREADY EXISTS")
