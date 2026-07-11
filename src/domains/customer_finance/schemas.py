from pydantic import BaseModel


class CreditUsageRequest(BaseModel):
    invoice_id: str
    amount: float
