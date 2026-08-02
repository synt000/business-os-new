from pydantic import BaseModel, ConfigDict
from typing import Optional


class CustomerIdentityCreate(BaseModel):
    customer_id: str
    provider: str
    external_user_id: str
    external_chat_id: Optional[str] = None


class CustomerIdentityLookup(BaseModel):
    provider: str
    external_user_id: str


class CustomerIdentityResponse(BaseModel):
    id: str
    tenant_id: str
    customer_id: str
    provider: str
    external_user_id: str
    external_chat_id: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True
    )
