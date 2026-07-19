import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc

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
from sqlalchemy import desc

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






@router.post("/approve/{purchase_id}")
def approve_purchase(
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
            "message":"PURCHASE_NOT_FOUND"
        }

    if po.status != "CONFIRMED":
        return {
            "status":"FAILED",
            "message":"INVALID_PURCHASE_STATUS"
        }

    po.status = "APPROVED"
    db.commit()

    return {
        "status":"SUCCESS",
        "message":"PURCHASE_APPROVED",
        "purchase_number":po.purchase_number
    }

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


    if po.status != "PENDING_APPROVAL":
        return {
            "status":"FAILED",
            "message":"INVALID_PURCHASE_STATUS"
        }


    # =========================
    # APPROVE AI PURCHASE
    # =========================

    po.status = "APPROVED"


    # =========================
    # CREATE PROCUREMENT LEDGER
    # =========================

    ledger = ProcurementLedger(
        id=str(uuid.uuid4()),
        tenant_id=current_user.tenant_id,
        purchase_order_id=po.id,
        amount=po.total_amount,
        status="APPROVED"
    )

    db.add(ledger)


    # =========================
    # CREATE ACCOUNT PAYABLE
    # =========================

    payable = AccountLedger(
        id=str(uuid.uuid4()),
        tenant_id=current_user.tenant_id,
        reference_id=po.id,
        reference_type="AI_PURCHASE_ORDER",
        amount=po.total_amount,
        entry_type="PAYABLE"
    )

    db.add(payable)


    db.commit()


    return {
        "status":"SUCCESS",
        "message":"AI Purchase Approved",
        "purchase_number":po.purchase_number,
        "next_step":"STOCK_RECEIVE_PENDING"
    }




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


    received = []

    for item in items:

        inventory = (
            db.query(Inventory)
            .filter(
                Inventory.product_id == item.product_id,
                Inventory.tenant_id == current_user.tenant_id
            )
            .first()
        )

        if not inventory:
            inventory = Inventory(
                product_id=item.product_id,
                quantity=0,
                tenant_id=current_user.tenant_id
            )
            db.add(inventory)
            db.flush()

        before = inventory.quantity

        inventory.quantity += item.quantity

        movement = StockMovement(
            id=str(uuid.uuid4()),
            product_id=item.product_id,
            movement_type="PURCHASE_RECEIVE",
            quantity_change=item.quantity,
            before_quantity=before,
            after_quantity=inventory.quantity,
            reason="Purchase Stock Received",
            tenant_id=current_user.tenant_id
        )

        db.add(movement)

        received.append({
            "product_id": item.product_id,
            "quantity": item.quantity
        })


    po.status = "RECEIVED"

    db.commit()


    return {
        "status":"SUCCESS",
        "message":"Purchase Stock Received",
        "purchase_number":po.purchase_number
    }


# ==========================================
# AI PURCHASE STOCK RECEIVE
# ==========================================

@router.post("/receive-ai-po/{purchase_id}")
def receive_ai_purchase_stock(
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


    if po.status != "APPROVED":
        return {
            "status":"FAILED",
            "message":"PURCHASE_NOT_READY"
        }


    items = (
        db.query(PurchaseItem)
        .filter(
            PurchaseItem.purchase_order_id == po.id,
            PurchaseItem.tenant_id == current_user.tenant_id
        )
        .all()
    )


    received = []


    for item in items:

        inventory = (
            db.query(Inventory)
            .filter(
                Inventory.product_id == item.product_id
            )
            .first()
        )


        if not inventory:
            inventory = Inventory(
                product_id=item.product_id,
                quantity=0
            )

            db.add(inventory)
            db.flush()


        before = inventory.quantity


        inventory.quantity += item.quantity


        movement = StockMovement(
            product_id=item.product_id,
            movement_type="PURCHASE_RECEIVE",
            quantity_change=item.quantity,
            before_quantity=before,
            after_quantity=inventory.quantity,
            reason="AI Purchase Receive",
            tenant_id=current_user.tenant_id
        )


        db.add(movement)


        received.append({
            "product_id":item.product_id,
            "quantity":item.quantity
        })


    po.status = "RECEIVED"


    db.commit()


    return {
        "status":"SUCCESS",
        "message":"AI Purchase Stock Received",
        "purchase_number":po.purchase_number,
        "items":received
    }

