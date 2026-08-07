from pathlib import Path

p = Path("src/product/router.py")
s = p.read_text()

old = '''    order.order_status = "PAID"

    db.commit()
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

        receivable = db.query(Receivable).filter(
            Receivable.invoice_id == invoice.id,
            Receivable.tenant_id == current_user.tenant_id
        ).first()

        if receivable:
            receivable.paid_amount = receivable.total_amount
            receivable.balance_amount = 0
            receivable.status = "PAID"

    db.commit()
'''

if old not in s:
    raise SystemExit("PAYMENT BLOCK NOT FOUND")

s = s.replace(old,new,1)

p.write_text(s)

print("PAYMENT INVOICE SYNC ADDED")
