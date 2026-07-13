from sqlalchemy.orm import Session

from src.models.saas_core import (
    Product,
    SupplierPayable,
)


def business_summary(
    db: Session,
    tenant_id: str
):

    product_count = (
        db.query(Product)
        .filter(
            Product.tenant_id == tenant_id
        )
        .count()
    )


    payable = (
        db.query(SupplierPayable)
        .filter(
            SupplierPayable.tenant_id == tenant_id
        )
        .all()
    )


    debt = sum(
        x.balance_amount
        for x in payable
    )


    return (
        "📊 Business Summary\n\n"
        f"Products: {product_count}\n"
        f"Supplier Debt: {debt}\n"
    )
