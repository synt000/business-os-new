from sqlalchemy.orm import Session

from src.domains.product.models import Product
from src.domains.inventory.models import StockMovement


def reduce_stock(
    db: Session,
    product: Product,
    quantity: int,
    reason: str = "Customer Order"
):

    if product.stock_qty < quantity:
        raise Exception("INSUFFICIENT_STOCK")


    before = product.stock_qty

    product.stock_qty -= quantity


    movement = StockMovement(
        product_id=product.id,
        tenant_id=product.tenant_id,
        movement_type="OUT",
        quantity_change=quantity,
        before_quantity=before,
        after_quantity=product.stock_qty,
        reason=reason
    )


    db.add(movement)

    return movement
