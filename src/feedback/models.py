from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime

from src.core.database import Base


class Feedback(Base):

    __tablename__ = "feedbacks"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    tenant_id = Column(
        String,
        index=True,
        nullable=False
    )


    user_id = Column(
        String,
        nullable=True
    )


    feedback_type = Column(
        String,
        nullable=False
    )


    subject = Column(
        String,
        nullable=False
    )


    message = Column(
        Text,
        nullable=False
    )


    status = Column(
        String,
        default="OPEN"
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
