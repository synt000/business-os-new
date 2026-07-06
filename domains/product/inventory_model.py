import uuid
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from infrastructure.db.base import Base

class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    tenant_id = Column(UUID(as_uuid=True), index=True, nullable=False)

    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"))

    # IN or OUT movement
    movement_type = Column(String, nullable=False)

    quantity = Column(Float, nullable=False)

    note = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
