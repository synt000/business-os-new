from sqlalchemy import func
from src.models.saas_core import Order


def packing_pending_widget(db, tenant_id):

    pending = (
        db.query(func.count(Order.id))
        .filter(
            Order.tenant_id == tenant_id,
            Order.order_status == "CONFIRMED"
        )
        .scalar()
    ) or 0


    return {
        "packing_pending": int(pending),
        "status": "READY"
    }
