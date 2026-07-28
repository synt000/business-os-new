import uuid

from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import TenantModel


class StockMovement(TenantModel):

    __tablename__ = "stock_movements"

    product_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("products.id"),
        nullable=False
    )


    before_quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    after_quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    quantity_change: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    movement_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    reason: Mapped[str] = mapped_column(
        String(255),
        nullable=True
    )

    product = relationship(
        "Product",
        back_populates="stock_movements"
    )
