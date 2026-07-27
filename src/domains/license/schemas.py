from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class LicenseCreate(BaseModel):
    tenant_id: str
    max_devices: int = 1
    expires_at: datetime


class LicenseActivate(BaseModel):
    license_key: str
    hardware_uid: str
    device_name: Optional[str] = None
    client_ip: Optional[str] = None


class LicenseDeviceBlock(BaseModel):
    device_id: str


class LicenseResponse(BaseModel):
    id: str
    key: str
    tenant_id: str
    max_devices: int
    expires_at: datetime
    is_active: bool

    class Config:
        from_attributes = True
