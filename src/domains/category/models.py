from sqlalchemy import String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import TenantModel


class Category(TenantModel):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    description: Mapped[str] = mapped_column(
        String(500),
        nullable=True
    )

    __table_args__ = (
        UniqueConstraint(
            "tenant_id",
            "name",
            name="uq_tenant_category_name"
        ),
    )

    products = relationship(
        "Product",
        back_populates="category"
    )

    tenant = relationship(
        "Tenant",
        back_populates="categories"
    )
