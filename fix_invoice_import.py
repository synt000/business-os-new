from pathlib import Path

p = Path("src/product/router.py")
s = p.read_text()

anchor = "from src.domains.invoice.schemas import InvoiceCreate\n"

add = """from src.models.saas_core import Invoice, Payment
"""

if "from src.models.saas_core import Invoice, Payment" not in s:
    s = s.replace(anchor, anchor + add)

p.write_text(s)

print("ADDED INVOICE MODEL IMPORT")
