from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    Text,
    Integer,
    DateTime,
    ForeignKey
)

from src.core.database import Base
import uuid


class CampaignExecutionLog(Base):

    __tablename__ = "campaign_execution_logs"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    campaign_id = Column(
        String,
        ForeignKey(
            "campaigns.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    status = Column(
        String(50),
        default="running"
    )

    attempt_count = Column(
        Integer,
        default=1
    )

    retry_count = Column(
        Integer,
        default=0
    )

    max_retries = Column(
        Integer,
        default=3
    )

    next_retry_at = Column(
        DateTime,
        nullable=True
    )

    worker_name = Column(
        String(100),
        default="campaign_scheduler"
    )

    error_message = Column(
        Text,
        nullable=True
    )

    started_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    completed_at = Column(
        DateTime,
        nullable=True
    )
