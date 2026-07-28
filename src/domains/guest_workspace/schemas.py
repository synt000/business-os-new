from datetime import datetime
from pydantic import BaseModel


class DeviceInfoCreate(BaseModel):
    device_fingerprint: str
    device_name: str | None = None
    platform: str | None = None
    browser: str | None = None
    screen_width: str | None = None
    screen_height: str | None = None
    timezone: str | None = None
    language: str | None = None
    ip_address: str | None = None
    user_agent: str | None = None


class GuestWorkspaceCreate(BaseModel):
    device: DeviceInfoCreate
    guest_name: str | None = "Guest"
    business_type_id: str | None = None


class GuestWorkspaceResponse(BaseModel):
    id: str
    workspace_key: str
    guest_name: str | None
    business_type_id: str | None
    created_at: datetime | None
    expires_at: datetime | None
    is_active: bool

    class Config:
        from_attributes = True


class GuestWorkspaceInfoResponse(BaseModel):
    workspace_key: str
    guest_name: str | None
    mode: str
    expires_at: datetime | None
    is_active: bool
    modules: list[str]
    require_signup: bool
