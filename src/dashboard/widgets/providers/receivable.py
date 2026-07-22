from sqlalchemy import func
from src.models.saas_core import Order


def receivable_widget(db, tenant_id):

    pending = (
        db.query(func.sum(Order.total_amount))
        .filter(
            Order.tenant_id == tenant_id,
            Order.order_status == "PENDING"
        )
        .scalar()
    ) or 0.0


    confirmed = (
        db.query(func.sum(Order.total_amount))
        .filter(
            Order.tenant_id == tenant_id,
            Order.order_status == "CONFIRMED"
        )
        .scalar()
    ) or 0.0


    return {
        "pending_amount": float(pending),
        "confirmed_amount": float(confirmed),
        "customer_debt": float(pending),
        "currency": "MMK"
    }
