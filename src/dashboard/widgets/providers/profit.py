from sqlalchemy import func
from src.models.saas_core import Order, OrderItem
from src.domains.product.models import Product


def profit_widget(db, tenant_id):

    revenue = (
        db.query(func.sum(Order.total_amount))
        .filter(
            Order.tenant_id == tenant_id
        )
        .scalar()
    ) or 0.0


    cost = (
        db.query(
            func.sum(
                OrderItem.quantity *
                Product.purchase_price
            )
        )
        .join(
            Product,
            Product.id == OrderItem.product_id
        )
        .join(
            Order,
            Order.id == OrderItem.order_id
        )
        .filter(
            Order.tenant_id == tenant_id
        )
        .scalar()
    ) or 0.0


    return {
        "revenue": float(revenue),
        "cost": float(cost),
        "gross_profit": float(revenue - cost),
        "currency": "MMK"
    }
