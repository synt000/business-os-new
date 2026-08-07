from pydantic import BaseModel


class CustomerPaymentCreate(BaseModel):
    payment_number: str
    receivable_id: str
    amount: float
    payment_method: str = "CASH"


class CustomerPaymentResponse(BaseModel):
    id: str
    payment_number: str
    customer_id: str
    receivable_id: str
    amount: float
    payment_method: str
    status: str

    class Config:
        from_attributes = True
