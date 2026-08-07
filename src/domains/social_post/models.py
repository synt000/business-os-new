from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    Text,
    DateTime,
    Boolean,
    ForeignKey
)

from src.core.database import Base
from src.models.saas_core import generate_uuid


class SocialPost(Base):

    __tablename__ = "social_posts"

    id = Column(
        String,
        primary_key=True,
        default=generate_uuid,
        index=True
    )

    tenant_id = Column(
        String,
        ForeignKey(
            "tenants.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    platform = Column(
        String,
        nullable=False,
        index=True
    )

    content = Column(
        Text,
        nullable=False
    )

    media_url = Column(
        Text,
        nullable=True
    )

    status = Column(
        String,
        default="draft",
        index=True
    )

    scheduled_at = Column(
        DateTime,
        nullable=True
    )

    published_at = Column(
        DateTime,
        nullable=True
    )

    created_by = Column(
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
