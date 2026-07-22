from sqlalchemy import func

try:
    from src.domains.product.models import Product
except ImportError:
    Product = None


def inventory_widget(db, tenant_id):
    if Product is None:
        return {
            "total_products": 0,
            "inventory_value": 0.0,
            "low_stock": 0,
            "out_of_stock": 0,
            "reorder": 0,
            "currency": "MMK",
            "status": "PRODUCT_MODEL_NOT_FOUND",
        }

    products = (
        db.query(Product)
        .filter(Product.tenant_id == tenant_id)
        .all()
    )

    total_products = len(products)

    inventory_value = sum(
        (getattr(p, "purchase_price", 0) or 0)
        for p in products
    )

    low_stock = sum(
        1 for p in products
        if (getattr(p, "reorder_level", 0) or 0) > 0
    )

    return {
        "total_products": total_products,
        "inventory_value": inventory_value,
        "low_stock": low_stock,
        "out_of_stock": 0,
        "reorder": low_stock,
        "currency": "MMK",
    }
