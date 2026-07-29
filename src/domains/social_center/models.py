from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    Boolean,
    DateTime,
    Text,
    ForeignKey
)

from src.core.database import Base
from src.models.saas_core import generate_uuid


class SocialChannel(Base):

    __tablename__ = "social_channels"


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
    # facebook
    # instagram
    # tiktok
    # telegram
    # whatsapp


    channel_name = Column(
        String,
        nullable=True
    )


    external_id = Column(
        String,
        nullable=True,
        index=True
    )
    # Facebook Page ID
    # Telegram Bot ID


    access_token = Column(
        Text,
        nullable=True
    )


    webhook_token = Column(
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
