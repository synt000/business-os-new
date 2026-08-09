from datetime import datetime
from pydantic import BaseModel


class SocialPostCreate(BaseModel):
    tenant_id: str
    channel_id: str | None = None
    platform: str
    content: str
    media_url: str | None = None
    scheduled_at: datetime | None = None
    created_by: str | None = None


class SocialPostResponse(BaseModel):
    id: str
    tenant_id: str
    channel_id: str | None = None
    platform: str
    content: str
    media_url: str | None = None
    status: str | None = None
    scheduled_at: datetime | None = None
    published_at: datetime | None = None
    created_by: str | None = None
    is_active: bool | None = None
    created_at: datetime | None = None

    class Config:
        from_attributes = True
