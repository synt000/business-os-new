from sqlalchemy import Column, Integer, String, Boolean, Text

from src.core.database import Base


class WebsiteSetting(Base):

    __tablename__ = "website_settings"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    logo_url = Column(
        String,
        nullable=True
    )

    live_message = Column(
        Text,
        nullable=True
    )

    contact_email = Column(
        String,
        nullable=True
    )

    telegram = Column(
        String,
        nullable=True
    )

    phone = Column(
        String,
        nullable=True
    )

    viber = Column(
        String,
        nullable=True
    )

    is_active = Column(
        Boolean,
        default=True
    )
