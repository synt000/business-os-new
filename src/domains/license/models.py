from datetime import datetime
import uuid

from sqlalchemy import (
    Column,
    String,
    Boolean,
    DateTime,
    Integer,
    ForeignKey
)

from src.core.database import Base


def generate_uuid():
    return str(uuid.uuid4())


class LicenseKey(Base):
    __tablename__ = "license_keys"

    id = Column(
        String,
        primary_key=True,
        default=generate_uuid
    )

    tenant_id = Column(
        String,
        ForeignKey("tenants.id"),
        nullable=False,
        index=True
    )

    key = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )

    max_devices = Column(
        Integer,
        default=1
    )

    expires_at = Column(
        DateTime,
        nullable=False
    )

    is_active = Column(
        Boolean,
        default=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class LicenseDevice(Base):
    __tablename__ = "license_devices"

    id = Column(
        String,
        primary_key=True,
        default=generate_uuid
    )

    license_id = Column(
        String,
        ForeignKey("license_keys.id"),
        nullable=False,
        index=True
    )

    hardware_uid = Column(
        String,
        nullable=False,
        index=True
    )

    device_name = Column(
        String,
        nullable=True
    )

    client_ip = Column(
        String,
        nullable=True
    )

    is_blocked = Column(
        Boolean,
        default=False
    )

    last_login = Column(
        DateTime,
        default=datetime.utcnow
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class LicenseEvent(Base):
    __tablename__ = "license_events"

    id = Column(
        String,
        primary_key=True,
        default=generate_uuid
    )

    license_id = Column(
        String,
        ForeignKey("license_keys.id"),
        nullable=False
    )

    event_type = Column(
        String,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
