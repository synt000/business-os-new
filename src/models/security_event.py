import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Text, Index

from src.core.database import Base


def generate_uuid():
    return str(uuid.uuid4())


class SecurityEvent(Base):
    __tablename__ = "security_events"

    id = Column(
        String,
        primary_key=True,
        default=generate_uuid,
        index=True
    )

    user_id = Column(
        String,
        nullable=True,
        index=True
    )

    tenant_id = Column(
        String,
        nullable=True,
        index=True
    )

    event_type = Column(
        String,
        nullable=False,
        index=True
    )

    severity = Column(
        String,
        default="INFO"
    )

    ip_address = Column(
        String,
        nullable=True
    )

    user_agent = Column(
        Text,
        nullable=True
    )

    device_info = Column(
        Text,
        nullable=True
    )

    description = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        index=True
    )


    __table_args__ = (
        Index(
            "idx_security_event_tenant_type",
            "tenant_id",
            "event_type"
        ),
    )
