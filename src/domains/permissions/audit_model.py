from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey
)

from datetime import datetime

from src.core.database import Base


class PermissionAuditLog(Base):

    __tablename__ = "permission_audit_logs"


    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )


    actor_user_id = Column(
        String,
        nullable=False
    )


    target_user_id = Column(
        String,
        nullable=False
    )


    permission_id = Column(
        Integer,
        nullable=False
    )


    action = Column(
        String,
        nullable=False
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
