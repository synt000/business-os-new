from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    DateTime,
    Boolean,
)

from src.core.database import Base


class WebhookEvent(Base):

    __tablename__ = "webhook_events"

    id = Column(
        String,
        primary_key=True,
    )

    event_id = Column(
        String,
        unique=True,
        nullable=False,
    )

    provider = Column(
        String,
        nullable=False,
    )

    processed = Column(
        Boolean,
        default=False,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )
