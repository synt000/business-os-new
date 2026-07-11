from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import get_db
from src.domains.inventory.schemas import InventoryResponse, InventoryCreate
from src.domains.inventory.repository import InventoryRepository

router = APIRouter(prefix="/inventory", tags=["inventory"])

@router.get("/{product_id}", response_model=InventoryResponse)
def get_stock(product_id: str, db: Session = Depends(get_db)):
    repo = InventoryRepository(db)
    inventory = repo.get_by_product(product_id)
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return inventory

@router.post("/", response_model=InventoryResponse)
def create_stock(data: InventoryCreate, db: Session = Depends(get_db)):
    repo = InventoryRepository(db)
    return repo.create(data)
