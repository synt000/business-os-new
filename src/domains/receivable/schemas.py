from pydantic import BaseModel


class ReceivableCreate(BaseModel):
    invoice_id: str
    customer_id: str


class ReceivablePaymentUpdate(BaseModel):
    amount: float


class ReceivableResponse(BaseModel):
    id: str
    customer_id: str
    invoice_id: str
    total_amount: float
    paid_amount: float
    balance_amount: float
    status: str

    class Config:
        from_attributes = True
