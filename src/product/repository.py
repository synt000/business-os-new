from sqlalchemy.orm import Session
from sqlalchemy.future import select
from src.domains.product.models import Product
from uuid import UUID

class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, product_id: UUID, tenant_id: UUID):
        stmt = select(Product).where(Product.id == product_id, Product.tenant_id == tenant_id)
        return self.db.execute(stmt).scalar_one_or_none()

    def get_by_sku(self, sku: str, tenant_id: UUID):
        stmt = select(Product).where(Product.sku == sku, Product.tenant_id == tenant_id)
        return self.db.execute(stmt).scalar_one_or_none()

    def create(self, product_data: dict):
        product = Product(**product_data)
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def update(self, product: Product, data: dict):
        for key, value in data.items():
            setattr(product, key, value)
        self.db.commit()
        self.db.refresh(product)
        return product

    def get_all(self, tenant_id: UUID):
        stmt = select(Product).where(Product.tenant_id == tenant_id)
        return self.db.execute(stmt).scalars().all()

    def delete(self, product: Product):
        self.db.delete(product)
        self.db.commit()
