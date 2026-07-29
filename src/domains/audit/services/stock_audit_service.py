from sqlalchemy.orm import Session
from sqlalchemy import func

from src.models.saas_core import Product
from src.domains.movement.models import StockMovement


def check_stock_consistency(
    db: Session,
    tenant_id: str,
):

    products = (
        db.query(Product)
        .filter(
            Product.tenant_id == tenant_id
        )
        .all()
    )

    issues = []

    for product in products:

        calculated_stock = (
            db.query(func.sum(StockMovement.quantity_change))
            .filter(
                StockMovement.product_id == product.id,
                StockMovement.tenant_id == tenant_id,
            )
            .scalar()
            or 0
        )


        if int(calculated_stock) != int(product.stock_quantity):

            issues.append(
                {
                    "type": "STOCK_CORRUPTION_ALERT",
                    "product_id": product.id,
                    "product_name": product.name,
                    "database_stock": product.stock_quantity,
                    "calculated_stock": calculated_stock,
                }
            )


    return {
        "status": "OK"
        if not issues else "FAILED",
        "issues": issues,
    }
