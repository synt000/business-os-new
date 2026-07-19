import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Boolean

from src.core.database import Base


class LoginSession(Base):

    __tablename__ = "login_sessions"


    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )


    user_id = Column(
        String,
        nullable=False,
        index=True
    )


    tenant_id = Column(
        String,
        nullable=False,
        index=True
    )


    session_key = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )


    device_name = Column(
        String,
        nullable=True
    )


    ip_address = Column(
        String,
        nullable=True
    )


    is_active = Column(
        Boolean,
        default=True
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


    last_used_at = Column(
        DateTime,
        default=datetime.utcnow
    )
