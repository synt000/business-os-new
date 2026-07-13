from sqlalchemy.orm import Session

from src.models.saas_core import Product


def stock_status(
    db: Session,
    tenant_id: str
):

    products = (
        db.query(Product)
        .filter(
            Product.tenant_id == tenant_id
        )
        .order_by(
            Product.stock_qty.asc()
        )
        .limit(10)
        .all()
    )


    if not products:
        return "No products found."


    result = "📦 Stock Status\n\n"


    for p in products:

        result += (
            f"{p.name}\n"
            f"Stock: {p.stock_qty}\n\n"
        )


    return result
