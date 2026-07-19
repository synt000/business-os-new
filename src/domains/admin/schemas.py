from pydantic import BaseModel
from typing import List, Optional


class TenantStatusUpdate(BaseModel):
    is_billing_active: bool


# =========================
# SUBSCRIPTION PLAN ADMIN
# =========================

class PlanCreate(BaseModel):
    name: str
    duration_days: int
    price: float = 0
    features: List[str] = []


class PlanUpdate(BaseModel):
    name: Optional[str] = None
    duration_days: Optional[int] = None
    price: Optional[float] = None
    features: Optional[List[str]] = None
    active: Optional[bool] = None


class PlanResponse(BaseModel):
    id: str
    name: str
    duration_days: int
    price: float
    features: List[str]
    active: bool


class FeatureAssignRequest(BaseModel):
    features: List[str]
