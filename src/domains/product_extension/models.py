from sqlalchemy import String, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import TenantModel


class ProductVariant(TenantModel):
    __tablename__ = "product_variants"

    product_id: Mapped[str] = mapped_column(
        ForeignKey("products.id"),
        nullable=False,
        index=True
    )

    variant_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    attributes: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True
    )


class ProductSKU(TenantModel):
    __tablename__ = "product_skus"

    product_id: Mapped[str] = mapped_column(
        ForeignKey("products.id"),
        nullable=False,
        index=True
    )

    variant_id: Mapped[str | None] = mapped_column(
        ForeignKey("product_variants.id"),
        nullable=True
    )

    sku_code: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True
    )

    barcode: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )


class ProductMedia(TenantModel):
    __tablename__ = "product_media"

    product_id: Mapped[str] = mapped_column(
        ForeignKey("products.id"),
        nullable=False,
        index=True
    )

    file_url: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    media_type: Mapped[str] = mapped_column(
        String(50),
        default="IMAGE"
    )
