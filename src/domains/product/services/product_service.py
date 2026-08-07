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


def create_product(
    db: Session,
    tenant_id: str,
    data
):
    product = Product(
        tenant_id=tenant_id,
        name=data.name,
        sku=data.sku,
        barcode=data.barcode,
        price=data.price,
        purchase_price=data.purchase_price,
        retail_price=data.retail_price,
        reorder_level=data.reorder_level,
        category_id=data.category_id,
        description=data.description,
        brand=data.brand,
        image_url=data.image_url,
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    return product
