from sqlalchemy.orm import Session

from src.domains.product.models import Product
from src.domains.inventory.models import Inventory
from src.domains.movement.models import StockMovement


class ProductWriteService:
    def __init__(self, db: Session):
        self.db = db

    def create_product_transaction(
        self,
        tenant_id,
        name: str,
        sku: str,
        barcode: str | None,
        purchase_price: int,
        retail_price: int,
        stock_qty: int,
    ):
        product = Product(
            tenant_id=tenant_id,
            name=name,
            sku=sku,
            barcode=barcode,
            price=retail_price,
            purchase_price=purchase_price,
            retail_price=retail_price,
        )

        self.db.add(product)
        self.db.flush()

        inventory = Inventory(
            tenant_id=tenant_id,
            product_id=product.id,
            quantity=stock_qty,
        )

        self.db.add(inventory)

        movement = StockMovement(
            tenant_id=tenant_id,
            product_id=product.id,
            movement_type="IN",
            quantity_change=stock_qty,
            before_quantity=0,
            after_quantity=stock_qty,
            reason="Initial product stock",
        )

        self.db.add(movement)

        return product
