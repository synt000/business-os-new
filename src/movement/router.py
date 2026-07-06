from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from infrastructure.db.session import get_db
from repositories.movement_repository import MovementRepository
from domains.movement.model import Movement
from pydantic import BaseModel
from uuid import UUID

router = APIRouter(prefix="/movements", tags=["movements"])

class MovementCreate(BaseModel):
    product_id: UUID
    quantity: float
    movement_type: str # "IN" or "OUT"

@router.post("/")
def log_movement(data: MovementCreate, request: Request, db: Session = Depends(get_db)):
    new_mv = Movement(tenant_id=request.state.tenant_id, **data.dict())
    return MovementRepository.log_movement(db, new_mv)
