from pydantic import BaseModel
from typing import Optional


class SupplierCreate(BaseModel):
    supplier_name: str
    contact_phone: Optional[str] = None


class SupplierResponse(BaseModel):
    id: str
    supplier_name: str
    contact_phone: Optional[str] = None

    class Config:
        from_attributes = True
