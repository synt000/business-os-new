from sqlalchemy.orm import Session

from src.models.saas_core import (
    Invoice,
    Order,
)

from src.domains.accounting.models import AccountLedger
from src.domains.audit.service import AuditService


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

    AuditService.create_audit_log(
        db=db,
        tenant_id=tenant_id,
        action="CREATE",
        table_name="invoices",
        record_id=str(invoice.id),
        changes=(
            f"invoice_number={invoice.invoice_number}, "
            f"amount={order.total_amount}, "
            f"status={invoice.status}, "
            f"ledger_reference={ledger.reference_id}"
        ),
    )

    db.commit()
    db.refresh(invoice)

    return invoice
