from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.dialects.postgresql import UUID

from src.database import TenantModel


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

    category_id = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("categories.id")
    )

    category = relationship(
        "Category",
        back_populates="products"
    )

    inventory = relationship(
        "Inventory",
        back_populates="product",
        uselist=False
    )

    tenant = relationship(
        "Tenant",
        back_populates="products"
    )
