import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.security import get_current_user

from src.models.saas_core import User
from src.domains.inventory.models import StockMovement, Inventory

from src.domains.purchase.schemas import (
    PurchaseCreate,
    PurchaseResponse,
)

from src.domains.purchase.services.purchase_service import (
    create_purchase,
)


router = APIRouter(
    prefix="/purchases",
    tags=["Purchases"]
)



@router.post(
    "/",
    response_model=PurchaseResponse
)
async def create_purchase_api(
    data: PurchaseCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    try:

        return create_purchase(
            db,
            current_user.tenant_id,
            data
        )

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


from fastapi import Depends
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.security import get_current_user

from src.models.saas_core import (
    User,
    PurchaseOrder,
    PurchaseItem,
    ProcurementLedger,
    AccountLedger,
)
from src.domains.product.models import Product


from src.domains.inventory.models import StockMovement, Inventory
@router.post("/approve-ai-po/{purchase_id}")
def approve_ai_purchase(
    purchase_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    po = (
        db.query(PurchaseOrder)
        .filter(
            PurchaseOrder.id == purchase_id,
            PurchaseOrder.tenant_id == current_user.tenant_id
        )
        .first()
    )

    if not po:
        return {
            "status":"FAILED",
            "message":"Purchase Order Not Found"
        }

    if po.status == "RECEIVED":
        return {
            "status":"FAILED",
            "message":"PURCHASE_ALREADY_RECEIVED"
        }

    if po.status in ["APPROVED", "RECEIVED"]:
        return {
            "status":"FAILED",
            "message":"PURCHASE_ALREADY_APPROVED"
        }

    po.status = "APPROVED"

    po.status = "APPROVED"

    db.commit()

    return {
        "status":"SUCCESS",
        "message":"Purchase Order Approved",
        "purchase_number":po.purchase_number
    }



from sqlalchemy import desc

from src.models.saas_core import PurchaseOrder
from src.domains.inventory.models import StockMovement, Inventory


@router.get("/orders")
def list_purchase_orders(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    rows = (
        db.query(PurchaseOrder)
        .filter(
            PurchaseOrder.tenant_id == current_user.tenant_id
        )
        .order_by(desc(PurchaseOrder.created_at))
        .all()
    )

    return [
        {
            "id": r.id,
            "purchase_number": r.purchase_number,
            "status": r.status,
            "supplier_id": r.supplier_id,
            "total_amount": r.total_amount,
            "created_at": r.created_at
        }
        for r in rows
    ]



@router.post("/receive/{purchase_id}")
def receive_purchase_stock(
    purchase_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    po = (
        db.query(PurchaseOrder)
        .filter(
            PurchaseOrder.id == purchase_id,
            PurchaseOrder.tenant_id == current_user.tenant_id
        )
        .first()
    )

    if not po:
        return {
            "status": "FAILED",
            "message": "Purchase Order Not Found"
        }


    if po.status == "RECEIVED":
        return {
            "status": "FAILED",
            "message": "PURCHASE_ALREADY_RECEIVED"
        }

    if po.status != "APPROVED":
        return {
            "status": "FAILED",
            "message": "PURCHASE_NOT_APPROVED"
        }


    items = (
        db.query(PurchaseItem)
        .filter(
            PurchaseItem.purchase_order_id == po.id
        )
        .all()
    )


    # STOCK RECEIVE moved to /receive endpoint
    # approve only changes status

    po.status = "RECEIVED"

    db.commit()


    return {
        "status":"SUCCESS",
        "message":"Purchase Stock Received",
        "purchase_number":po.purchase_number
    }
