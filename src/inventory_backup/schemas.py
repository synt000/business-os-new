from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class InventoryBase(BaseModel):
    product_id: UUID
    quantity: int = 0
    low_stock_threshold: int = 10
    warehouse_location: Optional[str] = None

class InventoryCreate(InventoryBase):
    pass

class InventoryUpdate(BaseModel):
    quantity: Optional[int] = None
    low_stock_threshold: Optional[int] = None
    warehouse_location: Optional[str] = None

class InventoryResponse(InventoryBase):
    id: UUID

    class Config:
        from_attributes = True
