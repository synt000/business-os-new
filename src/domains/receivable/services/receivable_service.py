from sqlalchemy.orm import Session

from src.models.saas_core import (
    Receivable,
    Invoice,
    Customer
)


def create_receivable(
    db: Session,
    tenant_id: str,
    invoice: Invoice,
    customer_id: str
):

    receivable = Receivable(
        customer_id=customer_id,
        invoice_id=invoice.id,
        total_amount=invoice.amount,
        paid_amount=0,
        balance_amount=invoice.amount,
        status="OPEN",
        tenant_id=tenant_id
    )

    db.add(receivable)
    db.commit()
    db.refresh(receivable)

    return receivable



def apply_payment_to_receivable(
    db: Session,
    receivable: Receivable,
    amount: float
):

    receivable.paid_amount += amount

    receivable.balance_amount = (
        receivable.total_amount
        - receivable.paid_amount
    )

    if receivable.balance_amount <= 0:
        receivable.balance_amount = 0
        receivable.status = "PAID"

    else:
        receivable.status = "PARTIAL"

    db.commit()
    db.refresh(receivable)

    return receivable
