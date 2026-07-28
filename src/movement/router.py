from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.permissions.subscription_guard import require_active_subscription

from src.repositories.movement_repository import MovementRepository
from src.domains.movement.models import StockMovement as Movement
from src.domains.product.models import Product
from src.domains.inventory.models import Inventory

from pydantic import BaseModel
from uuid import UUID


router = APIRouter(
    prefix="/movements",
    tags=["movements"]
)


class MovementCreate(BaseModel):
    product_id: UUID
    quantity: float
    movement_type: str
    reference: str | None = None


@router.post("/")
def log_movement(
    data: MovementCreate,
    request: Request,
    current_user = Depends(require_active_subscription()),
    db: Session = Depends(get_db)
):

    product = (
        db.query(Product)
        .filter(
            Product.id == str(data.product_id),
            Product.tenant_id == current_user.tenant_id
        )
        .first()
    )

    if not product:
        return {
            "status": "error",
            "detail": "Product not found"
        }


    inventory = (
        db.query(Inventory)
        .filter(
            Inventory.product_id == str(data.product_id),
            Inventory.tenant_id == current_user.tenant_id
        )
        .first()
    )

    if inventory:
        before_qty = inventory.quantity
    else:
        before_qty = 0

    if data.movement_type.upper() == "IN":
        after_qty = before_qty + data.quantity
    else:
        after_qty = before_qty - data.quantity


    new_mv = Movement(
        tenant_id=current_user.tenant_id,
        product_id=data.product_id,
        quantity_change=data.quantity,
        before_quantity=before_qty,
        after_quantity=after_qty,
        movement_type=data.movement_type,
        reason=data.reference
    )


    if inventory:
        inventory.quantity = after_qty

    return MovementRepository.log_movement(db, new_mv)
