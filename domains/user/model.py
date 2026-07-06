import uuid

from sqlalchemy import (
    Column,
    String,
    Boolean,
    DateTime,
    func,
    UniqueConstraint
)
from sqlalchemy.dialects.postgresql import UUID

from infrastructure.db.base import Base


class User(Base):
    __tablename__ = "users"

    __table_args__ = (
        UniqueConstraint(
            "tenant_id",
            "username",
            name="uq_tenant_username"
        ),
        UniqueConstraint(
            "tenant_id",
            "email",
            name="uq_tenant_email"
        ),
    )

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    tenant_id = Column(
        UUID(as_uuid=True),
        nullable=False,
        index=True
    )

    username = Column(
        String,
        nullable=False,
        index=True
    )

    email = Column(
        String,
        nullable=True,
        index=True
    )

    password_hash = Column(
        String,
        nullable=False
    )

    role = Column(
        String,
        nullable=False,
        default="staff"
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
