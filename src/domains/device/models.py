from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func

from src.core.database import Base


class TenantDevice(Base):
    __tablename__ = "tenant_devices"

    id = Column(
        String,
        primary_key=True
    )

    tenant_id = Column(
        String,
        ForeignKey("tenants.id"),
        nullable=False,
        index=True
    )

    user_id = Column(
        String,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    device_fingerprint = Column(
        String,
        nullable=False,
        index=True
    )

    device_name = Column(
        String,
        nullable=True
    )

    platform = Column(
        String,
        nullable=True
    )

    browser = Column(
        String,
        nullable=True
    )

    is_active = Column(
        Boolean,
        default=True
    )

    last_seen = Column(
        DateTime,
        server_default=func.now()
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )
