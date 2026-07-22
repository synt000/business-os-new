from src.models.saas_core import Order
from sqlalchemy import func


def cod_collection_widget(db, tenant_id):

    pending = (
        db.query(func.sum(Order.total_amount))
        .filter(
            Order.tenant_id == tenant_id,
            Order.order_status == "PENDING"
        )
        .scalar()
    ) or 0


    confirmed = (
        db.query(func.sum(Order.total_amount))
        .filter(
            Order.tenant_id == tenant_id,
            Order.order_status == "CONFIRMED"
        )
        .scalar()
    ) or 0


    completed = (
        db.query(func.sum(Order.total_amount))
        .filter(
            Order.tenant_id == tenant_id,
            Order.order_status == "COMPLETED"
        )
        .scalar()
    ) or 0


    return {
        "pending_amount": float(pending),
        "confirmed_amount": float(confirmed),
        "completed_amount": float(completed),
        "currency": "MMK"
    }
