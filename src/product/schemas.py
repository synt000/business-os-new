from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime

class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    sku: str = Field(..., min_length=3, max_length=50)
    barcode: Optional[str] = None
    category_id: str
    price: float = Field(..., gt=0)
    stock_quantity: int = Field(0, ge=0)
    reorder_level: int = Field(5, ge=0)

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    sku: Optional[str] = None
    barcode: Optional[str] = None
    category_id: Optional[str] = None
    price: Optional[float] = None
    stock_quantity: Optional[int] = None
    reorder_level: Optional[int] = None

class ProductResponse(ProductBase):
    id: UUID
    tenant_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
