from pathlib import Path

p = Path("src/main.py")
s = p.read_text()

old = "from src.domains.supplier_payment.router import router as supplier_payment_router"

new = old + "\nfrom src.domains.customer_payment.router import router as customer_payment_router"

if "customer_payment_router" not in s:
    s = s.replace(old, new)
    p.write_text(s)
    print("IMPORT ADDED")
else:
    print("ALREADY EXISTS")
