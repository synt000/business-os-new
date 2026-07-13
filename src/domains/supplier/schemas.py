from pydantic import BaseModel


class SupplierCreate(BaseModel):
    supplier_name: str
    contact_phone: str | None = None


class SupplierUpdate(BaseModel):
    supplier_name: str | None = None
    contact_phone: str | None = None


class SupplierResponse(BaseModel):
    id: str
    supplier_name: str
    contact_phone: str | None = None

    class Config:
        from_attributes = True
