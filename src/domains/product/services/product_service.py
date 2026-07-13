from sqlalchemy.orm import Session

from src.domains.product.models import Product


def get_products(
    db: Session,
    tenant_id: str
):
    products = (
        db.query(Product)
        .filter(Product.tenant_id == tenant_id)
        .all()
    )

    return {
        "total_products": len(products),
        "products": [
            {
                "id": p.id,
                "name": p.name,
                "price": p.price
            }
            for p in products
        ]
    }
