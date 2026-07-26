from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.security import get_current_user

from src.models.saas_core import User
from src.domains.purchase.models import PurchaseOrder, PurchaseItem
from src.domains.product.models import Product


router = APIRouter(
    prefix="/ai",
    tags=["AI Dashboard"]
)


@router.get("/pending-actions")
def pending_ai_actions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    orders = (
        db.query(PurchaseOrder)
        .filter(
            PurchaseOrder.tenant_id == current_user.tenant_id,
            PurchaseOrder.status == "PENDING_APPROVAL"
        )
        .all()
    )

    result = []

    for po in orders:

        item = (
            db.query(PurchaseItem)
            .filter(
                PurchaseItem.purchase_order_id == po.id
            )
            .first()
        )

        product_name = None
        qty = 0

        if item:
            product = (
                db.query(Product)
                .filter(
                    Product.id == item.product_id
                )
                .first()
            )

            if product:
                product_name = product.name

            qty = item.quantity


        result.append(
            {
                "type": "PURCHASE_ORDER",
                "id": po.id,
                "title": "Urgent Stock Purchase",
                "purchase_number": po.purchase_number,
                "product": product_name,
                "quantity": qty,
                "amount": po.total_amount,
                "status": po.status
            }
        )


    return result



@router.post("/approve-action/{purchase_id}")
def approve_ai_purchase_action(
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

    if po.status != "PENDING_APPROVAL":
        return {
            "status": "FAILED",
            "message": "INVALID_STATUS"
        }

    from src.domains.accounting.models import ProcurementLedger, AccountLedger
    from src.domains.purchase.models import SupplierPayable
    import uuid

    po.status = "APPROVED"

    item = (
        db.query(PurchaseItem)
        .filter(PurchaseItem.purchase_order_id == po.id)
        .first()
    )

    if item:
        db.add(
            ProcurementLedger(
                id=str(uuid.uuid4()),
                procurement_number=po.purchase_number,
                qty_purchased=item.quantity,
                unit_cost=item.unit_cost,
                total_cost=item.total_cost,
                product_id=item.product_id,
                supplier_id=po.supplier_id,
                tenant_id=current_user.tenant_id
            )
        )

        db.add(
            SupplierPayable(
                id=str(uuid.uuid4()),
                purchase_order_id=po.id,
                supplier_id=po.supplier_id,
                total_amount=po.total_amount,
                paid_amount=0,
                balance_amount=po.total_amount,
                status="OPEN",
                tenant_id=current_user.tenant_id
            )
        )

        db.add(
            AccountLedger(
                id=str(uuid.uuid4()),
                entry_type="CREDIT",
                account_head="SUPPLIER_PAYABLE",
                amount=po.total_amount,
                reference_id=po.id,
                description="AI Purchase Approval",
                tenant_id=current_user.tenant_id
            )
        )

    db.commit()

    return {
        "status": "SUCCESS",
        "message": "AI_PURCHASE_APPROVED_WITH_LEDGER",
        "purchase_number": po.purchase_number
    }


@router.post("/reject-action/{purchase_id}")
def reject_ai_purchase_action(
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

    if po.status != "PENDING_APPROVAL":
        return {
            "status": "FAILED",
            "message": "INVALID_STATUS"
        }


    po.status = "REJECTED"

    db.commit()

    return {
        "status": "SUCCESS",
        "message": "AI_PURCHASE_REJECTED",
        "purchase_number": po.purchase_number
    }
