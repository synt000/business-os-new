import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey

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

    user_agent = Column(
        String,
        nullable=True
    )

    refresh_jti = Column(
        String,
        nullable=True,
        index=True
    )

    device_session_id = Column(
        String,
        ForeignKey(
            "device_sessions.id",
            ondelete="SET NULL"
        ),
        nullable=True,
        index=True
    )

    login_at = Column(
        DateTime,
        nullable=True
    )

    last_seen = Column(
        DateTime,
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
        default=datetime.now(timezone.utc)
    )


    last_used_at = Column(
        DateTime,
        default=datetime.now(timezone.utc)
    )
