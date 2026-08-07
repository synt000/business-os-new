from pydantic import BaseModel


class PaymentCreate(BaseModel):
    payment_number: str
    invoice_id: str
    amount: float
    payment_method: str


class PaymentResponse(BaseModel):
    id: str
    payment_number: str
    amount: float
    payment_method: str
    status: str
    invoice_id: str

    class Config:
        from_attributes = True


class PaymentMethodConfigResponse(BaseModel):
    code: str
    name: str
    category: str
    ledger_account: str
    enabled: bool
    is_default: bool


class PaymentConfigUpdateRequest(BaseModel):
    payment_code: str
