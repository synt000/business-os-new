import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.security import get_current_user

from src.models.saas_core import User

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

    if po.status == "APPROVED":
        return {
            "status":"FAILED",
            "message":"PURCHASE_ALREADY_APPROVED"
        }

    po.status = "APPROVED"

    items = (
        db.query(PurchaseItem)
        .filter(
            PurchaseItem.purchase_order_id == po.id
        )
        .all()
    )

    for item in items:

        product = (
            db.query(Product)
            .filter(
                Product.id == item.product_id,
                Product.tenant_id == current_user.tenant_id
            )
            .first()
        )

        if product:
            print("FOUND PRODUCT:", product.name, product.stock_qty, item.quantity)
            product.stock_qty += item.quantity
            print("NEW STOCK:", product.stock_qty)

            ledger = ProcurementLedger(
                id=str(uuid.uuid4()),
                procurement_number=po.purchase_number,
                qty_purchased=item.quantity,
                unit_cost=item.unit_cost,
                total_cost=item.total_cost,
                product_id=product.id,
                supplier_id=po.supplier_id,
                tenant_id=current_user.tenant_id,
            )

            db.add(ledger)

            # ACCOUNTING LEDGER
            if item.total_cost <= 0:
                print("SKIP ZERO COST LEDGER:", item.product_id)
                continue

            inventory_ledger = AccountLedger(
                id=str(uuid.uuid4()),
                entry_type="DEBIT",
                account_head="INVENTORY_ASSET",
                amount=item.total_cost,
                reference_id=po.id,
                description=f"Purchased inventory via {po.purchase_number}",
                tenant_id=current_user.tenant_id,
            )

            payable_ledger = AccountLedger(
                id=str(uuid.uuid4()),
                entry_type="CREDIT",
                account_head="SUPPLIER_PAYABLE",
                amount=item.total_cost,
                reference_id=po.id,
                description=f"Supplier payable created via {po.purchase_number}",
                tenant_id=current_user.tenant_id,
            )

            db.add(inventory_ledger)
            db.add(payable_ledger)

        else:
            print("PRODUCT NOT FOUND:", item.product_id)

    db.commit()

    return {
        "status":"SUCCESS",
        "message":"Purchase Order Approved & Stock Received",
        "purchase_number":po.purchase_number
    }



from sqlalchemy import desc

from src.models.saas_core import PurchaseOrder


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

