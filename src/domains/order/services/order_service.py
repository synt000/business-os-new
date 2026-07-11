from sqlalchemy.orm import Session

from src.models.saas_core import Product, Order, OrderItem
from src.domains.inventory.services.stock_service import reduce_stock


def create_order(
    db: Session,
    tenant_id: str,
    order_number: str,
    items: list,
    customer_id: str | None = None,
    customer_name: str = "Customer",
    customer_phone: str | None = None,
):

    total = 0

    order = Order(
        order_number=order_number,
        platform_channel="SYSTEM",
        customer_name=customer_name,
        customer_phone=customer_phone,
        customer_id=customer_id,
        total_amount=0,
        order_status="CONFIRMED",
        tenant_id=tenant_id
    )

    db.add(order)
    db.flush()


    for item in items:

        product = db.query(Product).filter(
            Product.id == str(item.product_id),
            Product.tenant_id == tenant_id
        ).first()

        if not product:
            raise Exception("PRODUCT_NOT_FOUND")


        reduce_stock(
            db,
            product,
            item.quantity,
            "Customer Order"
        )


        line_total = item.quantity * item.price
        total += line_total


        order_item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=item.quantity,
            price_at_sale=item.price
        )

        db.add(order_item)


    order.total_amount = total

    db.commit()
    db.refresh(order)

    return order
