from pathlib import Path

p = Path("src/product/router.py")
s = p.read_text()

old_import = """from src.product.services.product_write_service import ProductWriteService
"""

new_import = """from src.product.services.product_write_service import ProductWriteService
from src.domains.invoice.schemas import InvoiceCreate
from src.domains.invoice.services.invoice_service import create_invoice
"""

if "from src.domains.invoice.schemas import InvoiceCreate" not in s:
    s = s.replace(old_import, new_import)

old_block = """    record_double_entry_accounting(db, current_user.tenant_id, "CREDIT", "INVENTORY_ASSET", computed_cogs_pool, new_order.id, f"Asset inventory reduction mapped from sales checkout {order_num}")
"""

new_block = """    record_double_entry_accounting(db, current_user.tenant_id, "CREDIT", "INVENTORY_ASSET", computed_cogs_pool, new_order.id, f"Asset inventory reduction mapped from sales checkout {order_num}")

    invoice_data = InvoiceCreate(
        order_id=new_order.id,
        invoice_number=f"INV-{new_order.order_number}"
    )

    create_invoice(
        db,
        current_user.tenant_id,
        invoice_data,
    )
"""

if "invoice_data = InvoiceCreate(" not in s:
    if old_block not in s:
        raise SystemExit("ORDER ACCOUNTING BLOCK NOT FOUND")
    s = s.replace(old_block, new_block)

p.write_text(s)

print("INVOICE HOOK PATCH APPLIED")
