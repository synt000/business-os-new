from pydantic import BaseModel
from typing import Optional


class BusinessProfileCreate(BaseModel):
    business_name: str
    logo_url: Optional[str] = None
    cover_url: Optional[str] = None
    description: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    qr_code: Optional[str] = None


class BusinessProfileResponse(BaseModel):
    id: int
    tenant_id: str
    business_name: str
    logo_url: Optional[str] = None
    cover_url: Optional[str] = None
    description: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    qr_code: Optional[str] = None

    class Config:
        from_attributes = True
