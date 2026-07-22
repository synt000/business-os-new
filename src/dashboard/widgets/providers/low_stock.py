from sqlalchemy.orm import Session

from src.domains.product.models import Product
from src.domains.inventory.models import Inventory


def low_stock_widget(
    db: Session,
    tenant_id: str
):

    rows = (
        db.query(
            Product.name,
            Inventory.quantity,
            Product.reorder_level
        )
        .join(
            Inventory,
            Inventory.product_id == Product.id
        )
        .filter(
            Product.tenant_id == tenant_id,
            Inventory.quantity <= Product.reorder_level
        )
        .all()
    )


    items = []

    for r in rows:
        items.append(
            {
                "name": r.name,
                "stock": r.quantity,
                "reorder_level": r.reorder_level
            }
        )


    return {
        "count": len(items),
        "items": items
    }
