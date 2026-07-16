from pydantic import BaseModel


class TenantStatusUpdate(BaseModel):
    is_billing_active: bool
