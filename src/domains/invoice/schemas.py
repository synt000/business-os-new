from pydantic import BaseModel


class InvoiceCreate(BaseModel):
    order_id: str
    invoice_number: str


class InvoiceResponse(BaseModel):
    id: str
    invoice_number: str
    amount: float
    status: str
    order_id: str

    class Config:
        from_attributes = True
