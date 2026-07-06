import uuid
from sqlalchemy import Column, String, Float, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from infrastructure.db.base import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    tenant_id = Column(UUID(as_uuid=True), index=True, nullable=False)

    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"))

    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)

    stock = Column(Float, default=0)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
