from sqlalchemy import Column, Integer, String, Text, Boolean
from src.core.database import Base


class BusinessProfile(Base):
    __tablename__ = "business_profiles"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    # Multi Tenant Isolation
    tenant_id = Column(
        String,
        nullable=False,
        index=True
    )


    # Public Identity
    business_slug = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )


    business_name = Column(
        String,
        nullable=False
    )


    # Homepage Content
    welcome_message = Column(
        Text,
        nullable=True
    )


    description = Column(
        Text,
        nullable=True
    )


    # Branding
    logo_url = Column(
        String,
        nullable=True
    )


    cover_url = Column(
        String,
        nullable=True
    )


    theme_color = Column(
        String,
        default="#111827"
    )


    # Business Contact
    phone = Column(
        String,
        nullable=True
    )


    address = Column(
        Text,
        nullable=True
    )


    email = Column(
        String,
        nullable=True
    )


    website_url = Column(
        String,
        nullable=True
    )


    # Owner Contact
    owner_name = Column(
        String,
        nullable=True
    )


    owner_phone = Column(
        String,
        nullable=True
    )


    # Social Contact
    facebook_username = Column(
        String,
        nullable=True
    )


    telegram_username = Column(
        String,
        nullable=True
    )


    viber_number = Column(
        String,
        nullable=True
    )


    # Legacy URL Support
    facebook_url = Column(
        String,
        nullable=True
    )


    telegram_url = Column(
        String,
        nullable=True
    )


    # QR
    qr_code = Column(
        String,
        nullable=True
    )


    # Public Access Control
    is_public = Column(
        Boolean,
        default=True
    )
