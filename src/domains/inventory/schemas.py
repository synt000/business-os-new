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


from pydantic import BaseModel


class StockAdjustmentCreate(BaseModel):
    product_id: str
    adjustment: int
    reason: str | None = None


class StockMovementResponse(BaseModel):
    id: UUID
    product_id: UUID
    movement_type: str
    quantity_change: int
    before_quantity: int
    after_quantity: int
    reason: str | None = None

    class Config:
        from_attributes = True


class LowStockAlertResponse(BaseModel):
    product_id: UUID
    product_name: str
    current_stock: int
    threshold: int
    status: str

    class Config:
        from_attributes = True


class InventorySummaryResponse(BaseModel):
    total_products: int
    total_stock_units: int
    low_stock_count: int
    out_of_stock_count: int
    recent_movements: int

