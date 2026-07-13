from pydantic import BaseModel


class SupplierPaymentCreate(BaseModel):
    payment_number: str
    payable_id: str
    amount: float
    payment_method: str = "CASH"


class SupplierPaymentResponse(BaseModel):
    id: str
    payment_number: str
    supplier_id: str
    payable_id: str
    amount: float
    payment_method: str
    status: str

    class Config:
        from_attributes = True
