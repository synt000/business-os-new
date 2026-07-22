from sqlalchemy import func
from src.models.saas_core import Order


def parcel_tracking_widget(db, tenant_id):

    pending = (
        db.query(func.count(Order.id))
        .filter(
            Order.tenant_id == tenant_id,
            Order.order_status == "PENDING"
        )
        .scalar()
    ) or 0


    shipping = (
        db.query(func.count(Order.id))
        .filter(
            Order.tenant_id == tenant_id,
            Order.order_status == "SHIPPING"
        )
        .scalar()
    ) or 0


    delivered = (
        db.query(func.count(Order.id))
        .filter(
            Order.tenant_id == tenant_id,
            Order.order_status == "COMPLETED"
        )
        .scalar()
    ) or 0


    return {
        "pending": int(pending),
        "shipping": int(shipping),
        "delivered": int(delivered),
    }
