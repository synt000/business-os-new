from sqlalchemy.orm import Session

from src.domains.product.models import Product
from src.domains.inventory.models import StockMovement


def reduce_stock(
    db: Session,
    product: Product,
    quantity: int,
    reason: str = "Customer Order"
):

    inventory = product.inventory

    if not inventory:
        raise Exception("INVENTORY_NOT_FOUND")


    if inventory.quantity < quantity:
        raise Exception("INSUFFICIENT_STOCK")


    before = inventory.quantity


    inventory.quantity -= quantity


    movement = StockMovement(
        product_id=product.id,
        tenant_id=product.tenant_id,
        movement_type="OUT",
        quantity_change=quantity,
        before_quantity=before,
        after_quantity=inventory.quantity,
        reason=reason
    )


    db.add(movement)

    return movement
