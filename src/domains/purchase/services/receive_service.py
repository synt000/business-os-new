from sqlalchemy.orm import Session

from src.domains.purchase.models import PurchaseOrder, PurchaseItem
from src.domains.inventory.models import Inventory
from src.domains.movement.models import StockMovement
from src.domains.product.models import Product
from src.domains.audit.service import AuditService


class PurchaseReceiveService:

    @staticmethod
    def receive(
        db: Session,
        purchase_id: str,
        current_user
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

        if po.status not in [
            "APPROVED",
            "CONFIRMED"
        ]:
            return {
                "status": "FAILED",
                "message": "INVALID_STATUS"
            }

        old_status = po.status

        try:

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


                product = (
                    db.query(Product)
                    .filter(
                        Product.id == item.product_id,
                        Product.tenant_id == current_user.tenant_id
                    )
                    .first()
                )

                if product:
                    product.purchase_price = item.unit_cost


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


        except Exception:
            db.rollback()
            raise
