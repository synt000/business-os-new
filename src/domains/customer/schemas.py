from pydantic import BaseModel, ConfigDict
from typing import Optional


class CustomerCreate(BaseModel):
    full_name: str
    phone: str
    email: Optional[str] = None
    address: Optional[str] = None


class CustomerUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    status: Optional[str] = None


class CustomerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    full_name: str
    phone: str
    email: Optional[str]
    address: Optional[str]
    total_orders: int
    total_spent: float
    reward_points: int
    status: str
