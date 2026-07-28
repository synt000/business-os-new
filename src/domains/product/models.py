from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.orm import relationship, mapped_column

from src.core.database import TenantModel

from src.domains.accounting.models import ProcurementLedger


class Product(TenantModel):
    __tablename__ = "products"

    name = mapped_column(
        String,
        nullable=False
    )

    sku = mapped_column(
        String,
        unique=True,
        nullable=False
    )

    barcode = mapped_column(
        String,
        nullable=True
    )

    price = mapped_column(
        Integer,
        nullable=False
    )

    purchase_price = mapped_column(
        Integer,
        default=0,
        nullable=False
    )

    retail_price = mapped_column(
        Integer,
        default=0,
        nullable=False
    )

    reorder_level = mapped_column(
        Integer,
        default=5,
        nullable=False
    )

    category_id = mapped_column(
        String,
        ForeignKey("categories.id")
    )

    category = relationship(
        "Category",
        back_populates="products"
    )

    # inventory relationship disabled temporarily


    inventory = relationship(
        "Inventory",
        back_populates="product",
        uselist=False
    )

    stock_movements = relationship(
        "StockMovement",
        back_populates="product",
        cascade="all, delete-orphan"
    )

    # order_items relationship removed
    # Order domain owns OrderItem relationship

    # procurements relationship disabled temporarily
# tenant relationship disabled (registry fix)


# Stock movement relationship
stock_movements = relationship(
    "StockMovement",
    back_populates="product"
)
