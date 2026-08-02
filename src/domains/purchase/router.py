from src.domains.accounting.models import AccountLedger
from src.domains.inventory.models import Inventory
from src.domains.movement.models import StockMovement

import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc

from src.core.database import get_db
from src.core.security import get_current_user

from src.models.saas_core import User

from src.domains.purchase.models import (
    PurchaseOrder,
    PurchaseItem,
    SupplierPayable,
    SupplierPayment,
)

from src.domains.accounting.models import (
    ProcurementLedger,
)

from src.domains.product.models import Product
from src.domains.audit.service import AuditService
from src.domains.purchase.services.purchase_service import create_purchase
from src.domains.purchase.schemas import PurchaseCreate


router = APIRouter(
    prefix="/purchases",
    tags=["Purchases"]
)


@router.post("/")
def create_purchase_api(
    data: PurchaseCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
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
        .order_by(
            desc(PurchaseOrder.created_at)
        )
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


@router.post("/approve/{purchase_id}")
@router.post("/approve-ai-po/{purchase_id}")
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
        raise HTTPException(
            status_code=404,
            detail="PURCHASE_NOT_FOUND"
        )

    if po.status not in [
        "CONFIRMED",
        "PENDING_APPROVAL"
    ]:
        raise HTTPException(
            status_code=400,
            detail="INVALID_STATUS"
        )


    po.status = "APPROVED"


    items = (
        db.query(PurchaseItem)
        .filter(
            PurchaseItem.purchase_order_id == po.id
        )
        .all()
    )

    if not items:
        raise HTTPException(
            status_code=400,
            detail="PURCHASE_ITEMS_NOT_FOUND"
        )

    item = items[0]

    ledger = ProcurementLedger(
        id=str(uuid.uuid4()),
        procurement_number=po.purchase_number,
        qty_purchased=item.quantity,
        unit_cost=item.unit_cost,
        total_cost=item.total_cost,
        product_id=item.product_id,
        supplier_id=po.supplier_id,
        tenant_id=current_user.tenant_id
    )

    db.add(ledger)


    account = AccountLedger(
        id=str(uuid.uuid4()),
        entry_type="PAYABLE",
        account_head="SUPPLIER_PAYABLE",
        amount=po.total_amount,
        reference_id=po.id,
        description="Purchase Approval",
        tenant_id=current_user.tenant_id
    )

    db.add(account)

    existing_payable = (
        db.query(SupplierPayable)
        .filter(
            SupplierPayable.purchase_order_id == po.id,
            SupplierPayable.tenant_id == current_user.tenant_id
        )
        .first()
    )

    if existing_payable:
        raise HTTPException(
            status_code=400,
            detail="SUPPLIER_PAYABLE_ALREADY_EXISTS"
        )

    supplier_payable = SupplierPayable(
        id=str(uuid.uuid4()),
        purchase_order_id=po.id,
        supplier_id=po.supplier_id,
        total_amount=po.total_amount,
        paid_amount=0,
        balance_amount=po.total_amount,
        status="OPEN",
        tenant_id=current_user.tenant_id
    )

    db.add(supplier_payable)

    db.commit()


    return {
        "status":"SUCCESS",
        "message":"PURCHASE_APPROVED",
        "purchase_number":po.purchase_number
    }



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
            "message": "PURCHASE_NOT_FOUND"
        }

    if po.status == "RECEIVED":
        return {
            "status": "FAILED",
            "message": "PURCHASE_ALREADY_RECEIVED"
        }

    if po.status not in ["APPROVED", "CONFIRMED"]:
        return {
            "status": "FAILED",
            "message": "INVALID_STATUS"
        }

    old_status = po.status

    items = (
        db.query(PurchaseItem)
        .filter(
            PurchaseItem.purchase_order_id == po.id
        )
        .all()
    )

    total_received = 0

    for item in items:
        total_received += item.quantity

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

        after = inventory.quantity

        movement = StockMovement(
            product_id=item.product_id,
            movement_type="PURCHASE_RECEIVE",
            quantity_change=item.quantity,
            before_quantity=before,
            after_quantity=after,
            reason=f"Purchase {po.purchase_number}",
            tenant_id=current_user.tenant_id
        )

        db.add(movement)

    po.status = "RECEIVED"

    AuditService.create_audit_log(
        db=db,
        tenant_id=current_user.tenant_id,
        action="RECEIVE",
        table_name="purchase_orders",
        record_id=str(po.id),
        changes=(
            f"status_before={old_status}, "
            f"status_after=RECEIVED, "
            f"items_count={len(items)}, "
            f"received_stock={total_received}"
        ),
        user_id=current_user.id,
    )

    db.commit()

    return {
        "status": "SUCCESS",
        "message": "STOCK_RECEIVED",
        "purchase_number": po.purchase_number
    }

