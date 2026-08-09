from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey
from datetime import datetime
import uuid

from src.core.database import Base


class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    tenant_id = Column(
        String,
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False
    )

    name = Column(
        String(255),
        nullable=False
    )

    content = Column(
        Text,
        nullable=False
    )

    status = Column(
        String(50),
        default="draft"
    )

    scheduled_at = Column(
        DateTime,
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


class CampaignChannel(Base):
    __tablename__ = "campaign_channels"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    campaign_id = Column(
        String,
        ForeignKey("campaigns.id", ondelete="CASCADE"),
        nullable=False
    )

    channel_id = Column(
        String,
        ForeignKey("social_channels.id", ondelete="CASCADE"),
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
