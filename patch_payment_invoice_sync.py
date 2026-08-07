from pathlib import Path

path = Path("src/product/router.py")

text = path.read_text()

old = '''    order.order_status = "PAID"

    db.commit()
    db.refresh(order)

    return {
'''

new = '''    order.order_status = "PAID"

    # ==========================================
    # PHASE 6.1 PAYMENT -> INVOICE SYNC
    # ==========================================
    invoice = db.query(Invoice).filter(
        Invoice.order_id == order.id,
        Invoice.tenant_id == current_user.tenant_id
    ).first()

    if invoice:
        invoice.status = "PAID"

        db.add(AuditLog(
            tenant_id=current_user.tenant_id,
            action="UPDATE",
            table_name="invoices",
            record_id=str(invoice.id),
            changes=(
                f"invoice_status={invoice.status}, "
                f"payment_sync=true, "
                f"order_id={order.id}"
            )
        ))

    db.commit()
    db.refresh(order)

    return {
'''

if old not in text:
    raise SystemExit("TARGET BLOCK NOT FOUND")

text = text.replace(old, new, 1)

path.write_text(text)

print("PATCHED PAYMENT INVOICE SYNC")
