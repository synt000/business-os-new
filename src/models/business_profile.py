from sqlalchemy import Column, String, Text, Boolean
from src.core.database import Base
import uuid


class BusinessProfile(Base):
    __tablename__ = "business_profiles"

    __table_args__ = {
        "extend_existing": True
    }

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    business_name = Column(
        String,
        nullable=False
    )

    logo_url = Column(
        String,
        nullable=True
    )

    phone = Column(
        String,
        nullable=True
    )

    address = Column(
        Text,
        nullable=True
    )

    description = Column(
        Text,
        nullable=True
    )

    tenant_id = Column(
        String,
        nullable=False,
        index=True
    )

    created_at = Column(
        Text,
        nullable=True
    )

    business_slug = Column(
        String,
        unique=True,
        nullable=True,
        index=True
    )

    welcome_message = Column(
        Text,
        nullable=True
    )

    cover_url = Column(
        Text,
        nullable=True
    )

    email = Column(
        Text,
        nullable=True
    )

    website_url = Column(
        Text,
        nullable=True
    )

    owner_name = Column(
        Text,
        nullable=True
    )

    owner_phone = Column(
        Text,
        nullable=True
    )

    facebook_username = Column(
        Text,
        nullable=True
    )

    telegram_username = Column(
        Text,
        nullable=True
    )

    viber_number = Column(
        Text,
        nullable=True
    )

    facebook_url = Column(
        Text,
        nullable=True
    )

    telegram_url = Column(
        Text,
        nullable=True
    )

    qr_code = Column(
        Text,
        nullable=True
    )

    theme_color = Column(
        String,
        default="#111827"
    )

    is_public = Column(
        Boolean,
        default=True
    )
