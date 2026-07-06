from sqlalchemy.orm import Session
from domains.product.inventory_model import Inventory

class InventoryRepository:

    @staticmethod
    def add_movement(db: Session, movement: Inventory):
        db.add(movement)
        db.commit()
        db.refresh(movement)
        return movement

    @staticmethod
    def list_by_product(db: Session, product_id: str, tenant_id: str):
        return db.query(Inventory).filter(
            Inventory.product_id == product_id,
            Inventory.tenant_id == tenant_id
        ).all()
