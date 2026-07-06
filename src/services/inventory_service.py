from sqlalchemy.orm import Session
from src.repositories.movement_repository import MovementRepository
from uuid import UUID

class InventoryService:
    @staticmethod
    def get_current_stock(db: Session, product_id: UUID, tenant_id: UUID):
        movements = MovementRepository.get_product_movements(db, product_id, tenant_id)
        stock = 0.0
        for m in movements:
            if m.movement_type == "IN":
                stock += m.quantity
            elif m.movement_type == "OUT":
                stock -= m.quantity
        return stock
