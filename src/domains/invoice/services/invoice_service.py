from sqlalchemy.orm import Session

from src.models.saas_core import (
    Invoice,
    Order,
)

from src.domains.audit.service import AuditService

from src.domains.accounting.services.journal_service import (
    create_invoice_journal,
)

from src.domains.receivable.services.receivable_service import (
    create_receivable,
)


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


    create_receivable(
        db=db,
        tenant_id=tenant_id,
        invoice=invoice,
        customer_id=order.customer_id,
    )


    create_invoice_journal(
        db=db,
        tenant_id=tenant_id,
        invoice_id=str(invoice.id),
        invoice_amount=order.total_amount,
    )


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
            f"receivable_created=true"
        ),
    )


    db.commit()
    db.refresh(invoice)

    return invoice
