from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from src.database import TenantModel

class Inventory(TenantModel):
    __tablename__ = "inventory"

    product_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("products.id"),
        unique=True,
        nullable=False
    )
    quantity: Mapped[int] = mapped_column(Integer, default=0)
    low_stock_threshold: Mapped[int] = mapped_column(Integer, default=10)
    warehouse_location: Mapped[str] = mapped_column(String, nullable=True)

    # Relationship to Product
    product = relationship("Product", back_populates="inventory")
