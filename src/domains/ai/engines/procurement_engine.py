from sqlalchemy.orm import Session

from src.domains.product.models import Product


def generate_procurement_recommendation(
    db: Session,
    tenant_id: str
):

    products = (
        db.query(Product)
        .filter(
            Product.tenant_id == tenant_id
        )
        .all()
    )


    recommendations = []


    for product in products:

        stock = 0

        if product.inventory:
            stock = product.inventory.quantity


        reorder = product.reorder_level or 0


        if stock <= reorder:

            suggested_qty = (
                reorder * 3
            )


            recommendations.append({

                "product_id":
                    str(product.id),

                "product_name":
                    product.name,

                "current_stock":
                    stock,

                "reorder_level":
                    reorder,

                "suggested_purchase":
                    suggested_qty,

                "reason":
                    "Stock below reorder level",

                "confidence":
                    90

            })


    return recommendations
