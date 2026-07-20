from src.domains.purchase.models import PurchaseOrder, PurchaseItem
from sqlalchemy.orm import Session

from src.domains.ai_insight.recommendation import (
    generate_ai_recommendations
)

from src.models.saas_core import (
    Supplier,
    AIActionLog
)

from src.domains.accounting.services.journal_service import (
    create_purchase_journal
)

from src.domains.product.models import Product
from src.domains.inventory.models import Inventory, StockMovement
from src.domains.accounting.models import ProcurementLedger


def generate_ai_actions(
    db: Session,
    tenant_id: str
):

    recommendations = generate_ai_recommendations(
        db,
        tenant_id
    )

    actions = []


    for item in recommendations:

        action = {
            "title": item["title"],
            "priority": item["priority"],
            "action": item["action"],
            "action_id": None
        }


        if item["title"] == "Urgent Stock Purchase":

            action["action_id"] = (
                "CREATE_PURCHASE_ORDER"
            )


        elif item["title"] == "Payment Monitoring":

            action["action_id"] = (
                "CHECK_PAYMENT"
            )


        elif item["title"] == "Sales Growth":

            action["action_id"] = (
                "CREATE_CAMPAIGN"
            )


        actions.append(action)


    return actions



def save_ai_action_log(
    db: Session,
    tenant_id: str,
    user_id: str,
    action_id: str,
    title: str,
    message: str
):
    log = AIActionLog(
        tenant_id=tenant_id,
        user_id=user_id,
        action_id=action_id,
        action_title=title,
        status="SUCCESS",
        result_message=message
    )

    db.add(log)
    db.commit()


def execute_ai_action(
    db: Session,
    tenant_id: str,
    user_id: str,
    action_id: str
):


    if action_id == "CREATE_PURCHASE_ORDER":

        product = (
            db.query(Product)
            .filter(
                Product.tenant_id == tenant_id
            )
            .first()
        )

        supplier = (
            db.query(Supplier)
            .filter(
                Supplier.tenant_id == tenant_id
            )
            .first()
        )

        if not product or not supplier:
            return {
                "status": "FAILED",
                "message":
                "No Product or Supplier Available"
            }


        purchase = PurchaseOrder(
            purchase_number="AI-AUTO-PO",
            supplier_id=supplier.id,
            total_amount=product.purchase_price * 10,
            status="PENDING_APPROVAL",
            tenant_id=tenant_id
        )

        db.add(purchase)
        db.flush()


        item = PurchaseItem(
            purchase_order_id=purchase.id,
            product_id=product.id,
            quantity=10,
            unit_cost=product.purchase_price,
            total_cost=product.purchase_price * 10,
            tenant_id=tenant_id
        )

        db.add(item)


        # ===== AI PURCHASE STOCK RECEIVE =====

        inventory = (
            db.query(Inventory)
            .filter(
                Inventory.product_id == product.id,
                Inventory.tenant_id == tenant_id
            )
            .first()
        )

        if inventory:
            before_qty = inventory.quantity
            inventory.quantity += 10
            after_qty = inventory.quantity
        else:
            before_qty = 0
            inventory = Inventory(
                product_id=product.id,
                quantity=10,
                tenant_id=tenant_id
            )
            db.add(inventory)
            after_qty = 10


        movement = StockMovement(
            product_id=product.id,
            movement_type="PURCHASE_RECEIVE",
            quantity_change=10,
            before_quantity=before_qty,
            after_quantity=after_qty,
            reason="AI Auto Purchase Receive",
            tenant_id=tenant_id
        )

        db.add(movement)


        create_purchase_journal(
            db=db,
            tenant_id=tenant_id,
            purchase_id=purchase.id,
            purchase_amount=purchase.total_amount
        )


        db.commit()


        message = (
            "AI Purchase Order Created Successfully"
        )

        save_ai_action_log(
            db,
            tenant_id,
            user_id,
            action_id,
            "Urgent Stock Purchase",
            message
        )

        return {
            "status": "READY",
            "message": message
        }


    if action_id == "CHECK_PAYMENT":

        message = "Payment Review Started"

        save_ai_action_log(
            db,
            tenant_id,
            user_id,
            action_id,
            "Payment Monitoring",
            message
        )

        return {
            "status": "READY",
            "message": message
        }


    if action_id == "CREATE_CAMPAIGN":

        message = "Customer Campaign Suggestion Created"

        save_ai_action_log(
            db,
            tenant_id,
            user_id,
            action_id,
            "Sales Growth",
            message
        )

        return {
            "status": "READY",
            "message": message
        }


    return {
        "status": "UNKNOWN",
        "message":
        "Unknown AI Action"
    }
