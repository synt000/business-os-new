from pydantic import BaseModel


class PaymentWebhookPayload(BaseModel):
    event_id: str
    provider: str
    payment_id: str
    tenant_id: str
    status: str
