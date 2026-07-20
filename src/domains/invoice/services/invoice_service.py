from sqlalchemy.orm import Session

from src.models.saas_core import (
    Invoice,
    Order,
)

from src.domains.accounting.models import AccountLedger


def create_invoice(
    db: Session,
    tenant_id: str,
    data,
):

    order = (
        db.query(Order)
        .filter(
            Order.id == data.order_id,
            Order.tenant_id == tenant_id,
        )
        .first()
    )

    if not order:
        raise Exception("ORDER_NOT_FOUND")


    invoice = Invoice(
        invoice_number=data.invoice_number,
        amount=order.total_amount,
        status="UNPAID",
        order_id=order.id,
        tenant_id=tenant_id,
    )

    db.add(invoice)
    db.flush()


    ledger = AccountLedger(
        entry_type="INCOME",
        account_head="SALES",
        amount=order.total_amount,
        reference_id=invoice.id,
        description=f"Invoice {invoice.invoice_number}",
        tenant_id=tenant_id,
    )

    db.add(ledger)

    db.commit()
    db.refresh(invoice)

    return invoice
