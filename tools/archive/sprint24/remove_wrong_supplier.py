from pathlib import Path

p = Path("src/domains/dashboard/service.py")

text = p.read_text()

text = text.replace(
"""from src.domains.purchase.models import (
    SupplierPayable,
    Supplier,
)""",
"""from src.domains.purchase.models import (
    SupplierPayable,
)"""
)

p.write_text(text)

print("✅ removed wrong Supplier import")
