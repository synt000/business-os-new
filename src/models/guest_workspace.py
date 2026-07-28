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


class GuestWorkspace(Base):
    __tablename__ = "guest_workspaces"

    id = Column(
        String,
        primary_key=True,
        default=generate_uuid,
        index=True,
    )

    workspace_key = Column(
        String,
        unique=True,
        nullable=False,
        index=True,
    )

    device_id = Column(
        String,
        nullable=False,
        index=True,
    )

    guest_name = Column(
        String,
        nullable=True,
    )

    business_type_id = Column(
        String,
        ForeignKey("business_types.id"),
        nullable=True,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )

    last_seen_at = Column(
        DateTime,
        default=datetime.utcnow,
    )

    expires_at = Column(
        DateTime,
        nullable=True,
    )

    is_active = Column(
        Boolean,
        default=True,
    )
