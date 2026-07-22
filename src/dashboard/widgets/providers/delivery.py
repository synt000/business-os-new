from src.models.saas_core import Order


def delivery_pending_widget(db, tenant_id):

    pending = (
        db.query(Order)
        .filter(
            Order.tenant_id == tenant_id,
            Order.order_status == "PENDING"
        )
        .count()
    )

    shipping = (
        db.query(Order)
        .filter(
            Order.tenant_id == tenant_id,
            Order.order_status == "CONFIRMED"
        )
        .count()
    )

    delivered = (
        db.query(Order)
        .filter(
            Order.tenant_id == tenant_id,
            Order.order_status == "COMPLETED"
        )
        .count()
    )

    return {
        "pending": pending,
        "shipping": shipping,
        "delivered": delivered
    }
