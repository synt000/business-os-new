from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime

from src.core.database import Base


class SecurityLog(Base):
    __tablename__ = "security_logs"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    tenant_id = Column(
        String,
        nullable=True,
        index=True
    )

    user_id = Column(
        String,
        nullable=True,
        index=True
    )

    event = Column(
        String,
        nullable=False
    )

    ip_address = Column(
        String,
        nullable=True
    )

    user_agent = Column(
        Text,
        nullable=True
    )

    request_id = Column(
        String,
        nullable=True,
        index=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
