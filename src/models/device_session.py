import uuid
from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    Boolean,
    DateTime,
    ForeignKey,
)

from src.core.database import Base


def generate_uuid():
    return str(uuid.uuid4())


class DeviceSession(Base):
    __tablename__ = "device_sessions"

    id = Column(
        String,
        primary_key=True,
        default=generate_uuid,
        index=True,
    )

    workspace_id = Column(
        String,
        ForeignKey("guest_workspaces.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    device_fingerprint = Column(
        String,
        unique=True,
        nullable=False,
        index=True,
    )

    device_name = Column(
        String,
        nullable=True,
    )

    platform = Column(
        String,
        nullable=True,
    )

    browser = Column(
        String,
        nullable=True,
    )

    screen_width = Column(
        String,
        nullable=True,
    )

    screen_height = Column(
        String,
        nullable=True,
    )

    timezone = Column(
        String,
        nullable=True,
    )

    language = Column(
        String,
        nullable=True,
    )

    ip_address = Column(
        String,
        nullable=True,
    )

    user_agent = Column(
        String,
        nullable=True,
    )

    first_seen = Column(
        DateTime,
        default=datetime.utcnow,
    )

    last_seen = Column(
        DateTime,
        default=datetime.utcnow,
    )

    is_blocked = Column(
        Boolean,
        default=False,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )
