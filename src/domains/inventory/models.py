import uuid

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import TenantModel


class Inventory(TenantModel):
    __tablename__ = "inventory"

    product_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )

    low_stock_threshold: Mapped[int] = mapped_column(
        Integer,
        default=10,
        nullable=False
    )

    warehouse_location: Mapped[str | None] = mapped_column(
        nullable=True
    )

    product = relationship(
        "Product",
        back_populates="inventory",
        uselist=False
    )
