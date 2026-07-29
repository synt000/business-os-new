from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    Integer,
    Text,
    DateTime,
    ForeignKey
)

from src.core.database import Base
from src.models.saas_core import generate_uuid


class CustomerLead(Base):

    __tablename__ = "customer_leads"


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


    customer_name = Column(
        String,
        nullable=False
    )


    customer_phone = Column(
        String,
        nullable=True
    )


    product_id = Column(
        String,
        nullable=True,
        index=True
    )


    quantity = Column(
        Integer,
        default=1
    )


    message = Column(
        Text,
        nullable=True
    )


    source = Column(
        String,
        default="website"
    )


    status = Column(
        String,
        default="NEW"
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        index=True
    )
