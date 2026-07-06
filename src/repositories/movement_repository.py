from sqlalchemy.orm import Session
from domains.movement.model import Movement
from uuid import UUID

class MovementRepository:
    @staticmethod
    def log_movement(db: Session, movement: Movement):
        db.add(movement)
        db.commit()
        db.refresh(movement)
        return movement

    @staticmethod
    def get_product_movements(db: Session, product_id: UUID, tenant_id: UUID):
        return db.query(Movement).filter(
            Movement.product_id == product_id,
            Movement.tenant_id == tenant_id
        ).all()
