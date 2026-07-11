from sqlalchemy.orm import Session
from sqlalchemy import func

from src.models.saas_core import (
    Customer,
    Invoice,
    Payment,
)


def get_customer_balance(
    db: Session,
    tenant_id: str,
    customer_id: str
):

    customer = (
        db.query(Customer)
        .filter(
            Customer.id == customer_id,
            Customer.tenant_id == tenant_id
        )
        .first()
    )

    if not customer:
        raise Exception("CUSTOMER_NOT_FOUND")


    total_invoice = (
        db.query(func.sum(Invoice.amount))
        .join(Invoice.order)
        .filter(
            Invoice.tenant_id == tenant_id,
            Invoice.order.has(
                customer_id=customer_id
            )
        )
        .scalar()
    ) or 0


    total_paid = (
        db.query(func.sum(Payment.amount))
        .join(Invoice)
        .join(Invoice.order)
        .filter(
            Payment.tenant_id == tenant_id,
            Invoice.order.has(
                customer_id=customer_id
            )
        )
        .scalar()
    ) or 0


    balance = total_invoice - total_paid

    return {
        "customer_id": customer.id,
        "customer_name": customer.customer_name,
        "total_invoice": float(total_invoice),
        "total_paid": float(total_paid),
        "outstanding_balance": float(balance),
        "customer_credit": float(max(total_paid - total_invoice, 0))
    }
