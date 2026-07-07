from sqlalchemy import String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import BaseModel

class Category(BaseModel):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=True)

    # Multi-tenant constraint: တစ်ခုတည်းသော Tenant အတွင်းမှာပဲ Name ကို Unique ဖြစ်စေရမယ်
    __table_args__ = (
        UniqueConstraint("tenant_id", "name", name="uq_tenant_category_name"),
    )

    # Relationship (String-based)
    products = relationship("Product", back_populates="category")
