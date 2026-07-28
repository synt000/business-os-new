from pydantic import BaseModel, ConfigDict
from typing import Optional


class CustomerCreate(BaseModel):
    name: str
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None


class CustomerResponse(BaseModel):
    id: str
    tenant_id: str
    customer_name: str
    customer_phone: Optional[str] = None
    customer_email: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True
    )
