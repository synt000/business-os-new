from sqlalchemy import Column, String, Float, DateTime
from sqlalchemy.sql import func

from src.core.database import Base


class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(String, primary_key=True)

    supplier_code = Column(String, unique=True, nullable=False)

    supplier_name = Column(String, nullable=False)

    contact_person = Column(String)

    phone = Column(String)

    email = Column(String)

    address = Column(String)

    opening_balance = Column(Float, default=0)

    current_balance = Column(Float, default=0)

    status = Column(String, default="ACTIVE")

    notes = Column(String)

    tenant_id = Column(String, nullable=False)

    created_at = Column(
        DateTime,
        server_default=func.now()
    )

    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )
