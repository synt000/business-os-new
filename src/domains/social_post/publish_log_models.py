from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    Text,
    DateTime,
    Boolean,
    ForeignKey,
)

from src.core.database import Base
from src.models.saas_core import generate_uuid


class SocialPublishLog(Base):
    __tablename__ = "social_publish_logs"

    id = Column(
        String,
        primary_key=True,
        default=generate_uuid,
        index=True
    )

    post_id = Column(
        String,
        ForeignKey(
            "social_posts.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    channel_id = Column(
        String,
        ForeignKey(
            "social_channels.id",
            ondelete="CASCADE"
        ),
        nullable=True,
        index=True
    )

    platform = Column(
        String,
        nullable=False,
        index=True
    )

    success = Column(
        Boolean,
        default=False
    )

    response = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
