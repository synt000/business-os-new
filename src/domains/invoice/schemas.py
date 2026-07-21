from pydantic import BaseModel
from typing import Optional


class InvoiceCreate(BaseModel):
    order_id: Optional[str] = None
    invoice_number: str


class InvoiceResponse(BaseModel):
    id: str
    invoice_number: str
    amount: float
    status: str
    order_id: Optional[str] = None
    subscription_id: Optional[str] = None

    class Config:
        from_attributes = True


class InvoiceListResponse(BaseModel):
    invoices: list[InvoiceResponse]

    class Config:
        from_attributes = True
