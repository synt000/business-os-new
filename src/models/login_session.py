from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
)

from src.core.database import Base


class LoginSession(Base):
    __tablename__ = "login_sessions"

    id = Column(Integer, primary_key=True, autoincrement=True)

    tenant_id = Column(
        String,
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    user_id = Column(
        String,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    ip_address = Column(
        String,
        default="UNKNOWN"
    )

    user_agent = Column(
        String,
        default="UNKNOWN"
    )

    device_name = Column(
        String,
        default="UNKNOWN"
    )

    login_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    last_seen = Column(
        DateTime,
        default=datetime.utcnow
    )

    logout_at = Column(
        DateTime,
        nullable=True
    )

    is_active = Column(
        Boolean,
        default=True
    )

    refresh_jti = Column(
        String,
        nullable=True,
        index=True
    )
