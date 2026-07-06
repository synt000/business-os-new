import uuid
from sqlalchemy import Column, String, Float, ForeignKey, func, DateTime
from sqlalchemy.dialects.postgresql import UUID
from infrastructure.db.base import Base

class Movement(Base):
    __tablename__ = "movements"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
    quantity = Column(Float, nullable=False)
    movement_type = Column(String, nullable=False)  # "IN" or "OUT"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
