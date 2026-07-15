from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.domains.inventory.schemas import (
    StockAdjustmentCreate,
    StockMovementResponse,
    LowStockAlertResponse
)
from src.models.saas_core import User
from src.domains.inventory.models import StockMovement

from src.core.security import get_current_user
from src.domains.inventory.schemas import (
    StockAdjustmentCreate,
    StockMovementResponse,
    LowStockAlertResponse,
    InventorySummaryResponse
)


router = APIRouter(
    prefix="/inventory",
    tags=["inventory"]
)


@router.post("/adjust")
async def adjust_stock(
    data: StockAdjustmentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):



    if not product:
        raise HTTPException(
            status_code=404,
            detail="PRODUCT_NOT_FOUND"
        )


    old_qty = product.stock_qty
    new_qty = old_qty + data.adjustment


    if new_qty < 0:
        raise HTTPException(
            status_code=400,
            detail="INSUFFICIENT_STOCK"
        )


    # Update current stock
    product.stock_qty = new_qty


    # Create inventory history record
    movement = StockMovement(
        tenant_id=current_user.tenant_id,
        product_id=product.id,
        movement_type="IN" if data.adjustment > 0 else "OUT",
        quantity_change=data.adjustment,
        before_quantity=old_qty,
        after_quantity=new_qty,
        reason=data.reason
    )


    db.add(movement)

    db.commit()

    db.refresh(product)


    return {
        "status": "STOCK_ADJUSTED",
        "product_id": product.id,
        "old_quantity": old_qty,
        "adjustment": data.adjustment,
        "new_quantity": product.stock_qty,
        "reason": data.reason
    }


@router.get(
    "/movements/{product_id}",
    response_model=list[StockMovementResponse]
)
async def get_stock_movements(
    product_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    movements = db.query(StockMovement).filter(
        StockMovement.product_id == product_id,
        StockMovement.tenant_id == current_user.tenant_id
    ).order_by(
        StockMovement.created_at.desc()
    ).all()

    return movements


@router.get(
    "/alerts/low-stock",
    response_model=list[LowStockAlertResponse]
)
async def low_stock_alerts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    products = (
        db.query(Product)
        .filter(
            Product.tenant_id == current_user.tenant_id,
            Product.stock_qty <= Product.low_stock_threshold
        )
        .all()
    )

    return [
        {
            "product_id": p.id,
            "product_name": p.name,
            "current_stock": p.stock_qty,
            "threshold": p.low_stock_threshold,
            "status": "LOW_STOCK"
        }
        for p in products
    ]


@router.get(
    "/summary",
    response_model=InventorySummaryResponse
)
async def inventory_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    products = (
        db.query(Product)
        .filter(
            Product.tenant_id == current_user.tenant_id
        )
        .all()
    )


    total_products = len(products)

    total_stock_units = sum(
        p.stock_qty for p in products
    )


    low_stock_count = len([
        p for p in products
        if p.stock_qty <= p.low_stock_threshold
    ])


    out_of_stock_count = len([
        p for p in products
        if p.stock_qty == 0
    ])


    recent_movements = db.query(
        StockMovement
    ).filter(
        StockMovement.tenant_id == current_user.tenant_id
    ).count()


    return {
        "total_products": total_products,
        "total_stock_units": total_stock_units,
        "low_stock_count": low_stock_count,
        "out_of_stock_count": out_of_stock_count,
        "recent_movements": recent_movements
    }

