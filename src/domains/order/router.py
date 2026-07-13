from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.security import get_current_user
from src.models.saas_core import User, Order, Product

from src.domains.order.schemas import (
    OrderCreate,
    OrderResponse,
    OrderStatusUpdate,
)

from src.domains.order.services.order_service import create_order

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


@router.get("/")
async def list_orders():
    return {
        "status": "ORDER_MODULE_READY"
    }


@router.post(
    "/",
    response_model=OrderResponse
)
async def create_new_order(
    data: OrderCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:

        order = create_order(
            db,
            current_user.tenant_id,
            data.order_number,
            data.items,
            data.customer_id,
            data.customer_name,
            data.customer_phone,
        )

        return order

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.get("/list")
async def get_orders(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    orders = (
        db.query(Order)
        .filter(
            Order.tenant_id == current_user.tenant_id
        )
        .order_by(Order.created_at.desc())
        .all()
    )

    return [
        {
            "id": o.id,
            "order_number": o.order_number,
            "status": o.order_status,
            "total_amount": o.total_amount,
            "created_at": o.created_at,
        }
        for o in orders
    ]


@router.get("/detail/{order_id}")
async def get_order_detail(
    order_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    order = (
        db.query(Order)
        .filter(
            Order.id == order_id,
            Order.tenant_id == current_user.tenant_id
        )
        .first()
    )

    if not order:
        raise HTTPException(
            status_code=404,
            detail="ORDER_NOT_FOUND"
        )

    items = []

    for item in order.items:

        product = (
            db.query(Product)
            .filter(Product.id == item.product_id)
            .first()
        )

        items.append(
            {
                "product_id": item.product_id,
                "product_name": product.name if product else None,
                "quantity": item.quantity,
                "price": item.price_at_sale,
            }
        )

    return {
        "id": order.id,
        "order_number": order.order_number,
        "customer_id": order.customer_id,
        "customer_name": order.customer_name,
        "customer_phone": order.customer_phone,
        "status": order.order_status,
        "total_amount": order.total_amount,
        "items": items,
    }
