from pydantic import BaseModel
from typing import Optional, List


class SecurityEventItem(BaseModel):
    event: Optional[str] = None
    risk: Optional[str] = None
    score: Optional[str] = None
    login_session_id: Optional[str] = None
    device_session_id: Optional[str] = None
    time: Optional[str] = None


class SecurityOverviewResponse(BaseModel):
    security_status: str = "SECURE"
    today_new_devices: int = 0
    medium_risk_logins: int = 0
    high_risk_logins: int = 0
    blocked_devices: int = 0
    latest_events: List[SecurityEventItem] = []


class SecurityEventsResponse(BaseModel):
    events: List[SecurityEventItem] = []


class SecurityDeviceItem(BaseModel):
    id: str
    device_name: Optional[str] = None
    platform: Optional[str] = None
    browser: Optional[str] = None
    screen_width: Optional[str] = None
    screen_height: Optional[str] = None
    timezone_name: Optional[str] = None
    language: Optional[str] = None
    ip_address: Optional[str] = None
    first_seen: Optional[str] = None
    last_seen: Optional[str] = None
    is_blocked: bool = False


class SecurityDevicesResponse(BaseModel):
    devices: List[SecurityDeviceItem] = []
