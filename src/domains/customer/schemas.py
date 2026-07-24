from pydantic import BaseModel, ConfigDict
from typing import Optional


class CustomerCreate(BaseModel):
    full_name: str
    phone: str
    email: Optional[str] = None


class CustomerUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None


class CustomerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    customer_name: str
    customer_phone: Optional[str] = None
    customer_email: Optional[str] = None
    total_spent: float = 0.0
