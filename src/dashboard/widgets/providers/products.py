from sqlalchemy import func

from src.domains.product.models import Product
from src.models.saas_core import OrderItem, Order


def top_products_widget(db, tenant_id):

    rows = (
        db.query(
            Product.name.label("name"),
            func.sum(OrderItem.quantity).label("sold"),
            func.sum(
                OrderItem.quantity * OrderItem.price_at_sale
            ).label("revenue")
        )
        .join(
            OrderItem,
            OrderItem.product_id == Product.id
        )
        .join(
            Order,
            Order.id == OrderItem.order_id
        )
        .filter(
            Product.tenant_id == tenant_id
        )
        .group_by(
            Product.name
        )
        .order_by(
            func.sum(OrderItem.quantity).desc()
        )
        .limit(5)
        .all()
    )


    return {
        "items": [
            {
                "name": r.name,
                "sold": int(r.sold or 0),
                "revenue": float(r.revenue or 0)
            }
            for r in rows
        ]
    }
