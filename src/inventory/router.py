from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from infrastructure.db.session import get_db
from services.inventory_service import InventoryService
from uuid import UUID

router = APIRouter(prefix="/inventory", tags=["inventory"])

@router.get("/stock/{product_id}")
def get_stock(product_id: UUID, request: Request, db: Session = Depends(get_db)):
    stock = InventoryService.get_current_stock(db, product_id, request.state.tenant_id)
    return {"product_id": product_id, "current_stock": stock}
