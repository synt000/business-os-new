import uuid

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import TenantModel
from src.domains.product.models import Product


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


class StockMovement(TenantModel):
    __tablename__ = "stock_movements"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )

    product_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    movement_type: Mapped[str] = mapped_column(
        nullable=False
    )

    quantity_change: Mapped[int] = mapped_column(
        Integer,
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

    reason: Mapped[str | None] = mapped_column(
        nullable=True
    )


    product = relationship(
        "Product"
    )
