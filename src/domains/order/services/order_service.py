from sqlalchemy.orm import Session

from src.models.saas_core import Order, OrderItem
from src.domains.product.models import Product
from src.domains.inventory.services.stock_service import reduce_stock
from src.domains.accounting.services.accounting_service import create_sale_journal


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

        product_id = (
            item['product_id']
            if isinstance(item, dict)
            else item.product_id
        )

        print("DEBUG ITEM TYPE:", type(item))
        print("DEBUG ITEM:", item)

        product_id = (
            item['product_id']
            if isinstance(item, dict)
            else item.product_id
        )

        print("DEBUG PRODUCT ID:", product_id)
        print("DEBUG TENANT:", tenant_id)

        product = (
            db.query(Product)
            .filter(
                Product.id == str(product_id),
                Product.tenant_id == tenant_id
            )
            .first()
        )
        print("DEBUG FOUND PRODUCT:", product)

        print(
            "DEBUG SAME ID COUNT:",
            db.query(Product)
            .filter(Product.id == product_id)
            .count()
        )

        print(
            "DEBUG TENANT COUNT:",
            db.query(Product)
            .filter(Product.tenant_id == tenant_id)
            .count()
        )

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

    inventory_cost = 0

    for item in items:
        product_id = item['product_id'] if isinstance(item, dict) else item.product_id

        product = (
            db.query(Product)
            .filter(
                Product.id == str(product_id),
                Product.tenant_id == tenant_id
            )
            .first()
        )

        if product:
            qty = item['quantity'] if isinstance(item, dict) else item.quantity
            inventory_cost += product.purchase_price * qty

    create_sale_journal(
        db=db,
        tenant_id=tenant_id,
        order_id=order.id,
        sale_amount=total,
        inventory_cost=inventory_cost,
    )

    db.commit()
    db.refresh(order)

    return order
