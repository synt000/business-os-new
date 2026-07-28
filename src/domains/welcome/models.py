from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    Boolean,
    DateTime,
    Text,
)

from src.core.database import Base


class WelcomeSetting(Base):

    __tablename__ = "welcome_settings"

    id = Column(
        String,
        primary_key=True
    )

    language = Column(
        String,
        nullable=False,
        default="my"
    )

    title = Column(
        String,
        nullable=False,
        default="Business OS"
    )

    subtitle = Column(
        Text,
        nullable=True
    )

    hero_message = Column(
        Text,
        nullable=True
    )

    faq_content = Column(
        Text,
        nullable=True
    )

    features_json = Column(
        Text,
        nullable=True
    )

    button_text = Column(
        String,
        nullable=True,
        default="Continue"
    )

    live_banner = Column(
        Text,
        nullable=True
    )

    banner_active = Column(
        Boolean,
        default=True
    )

    logo_url = Column(
        Text,
        nullable=True
    )

    hero_image_url = Column(
        Text,
        nullable=True
    )

    theme_color = Column(
        String,
        default="#2563eb"
    )

    seo_title = Column(
        Text,
        nullable=True
    )

    seo_description = Column(
        Text,
        nullable=True
    )

    sections_json = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
