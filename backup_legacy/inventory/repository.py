from sqlalchemy.orm import Session
from src.inventory.models import Inventory
from src.inventory.schemas import InventoryCreate

class InventoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_product(self, product_id: str):
        return self.db.query(Inventory).filter(Inventory.product_id == product_id).first()

    def create(self, inventory_data: InventoryCreate):
        db_inventory = Inventory(**inventory_data.dict())
        self.db.add(db_inventory)
        self.db.commit()
        self.db.refresh(db_inventory)
        return db_inventory
