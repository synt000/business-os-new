from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class SubscriptionPlanCreate(BaseModel):
    id: str
    name: str
    duration_days: int
    price: float = 0
    features_json: str = "{}"


class SubscriptionPlanResponse(BaseModel):
    id: str
    name: str
    duration_days: int
    price: float
    features_json: str

    class Config:
        from_attributes = True


class StartSubscriptionRequest(BaseModel):
    tenant_id: str
    plan_id: str
    is_trial: bool = False


class SubscriptionResponse(BaseModel):
    id: str
    tenant_id: str
    plan_id: str
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    status: str
    is_trial: bool

    class Config:
        from_attributes = True


class SubscriptionPaymentCreate(BaseModel):
    plan_id: str
    method: str
    transaction_ref: Optional[str] = None


class SubscriptionPaymentResponse(BaseModel):
    id: str
    tenant_id: str
    plan_id: Optional[str] = None
    subscription_id: str
    method: str
    amount: float
    transaction_ref: Optional[str] = None
    status: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
