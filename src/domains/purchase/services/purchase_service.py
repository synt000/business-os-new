from sqlalchemy.orm import Session

from src.models.saas_core import (
    ProcurementLedger,
    Supplier,
    Product,
)

from src.domains.inventory.models import StockMovement


def create_purchase(
    db: Session,
    tenant_id: str,
    data,
):
    supplier = (
        db.query(Supplier)
        .filter(
            Supplier.id == data.supplier_id,
            Supplier.tenant_id == tenant_id,
        )
        .first()
    )

    if not supplier:
        raise Exception("SUPPLIER_NOT_FOUND")

    product = (
        db.query(Product)
        .filter(
            Product.id == data.product_id,
            Product.tenant_id == tenant_id,
        )
        .first()
    )

    if not product:
        raise Exception("PRODUCT_NOT_FOUND")

    before_quantity = product.stock_qty

    total_cost = data.qty_purchased * data.unit_cost

    purchase = ProcurementLedger(
        procurement_number=data.procurement_number,
        supplier_id=supplier.id,
        product_id=product.id,
        qty_purchased=data.qty_purchased,
        unit_cost=data.unit_cost,
        total_cost=total_cost,
        tenant_id=tenant_id,
    )

    product.stock_qty += data.qty_purchased

    movement = StockMovement(
        product_id=product.id,
        movement_type="IN",
        quantity_change=data.qty_purchased,
        before_quantity=before_quantity,
        after_quantity=product.stock_qty,
        reason=f"PURCHASE_{data.procurement_number}",
        tenant_id=tenant_id,
    )

    db.add(purchase)
    db.add(movement)

    db.commit()
    db.refresh(purchase)

    return purchase
