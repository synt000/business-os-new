from pydantic import BaseModel


class PaymentCreateRequest(BaseModel):

    provider: str

    amount: float

    reference: str
