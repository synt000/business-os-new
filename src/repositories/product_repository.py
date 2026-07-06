from sqlalchemy.orm import Session
from domains.product.model import Product
from uuid import UUID

class ProductRepository:

    @staticmethod
    def create(db: Session, product: Product):
        db.add(product)
        db.commit()
        db.refresh(product)
        return product

    @staticmethod
    def get_all_by_tenant(db: Session, tenant_id: UUID):
        return db.query(Product).filter(Product.tenant_id == tenant_id).all()

    @staticmethod
    def get_by_id(db: Session, product_id: UUID, tenant_id: UUID):
        return db.query(Product).filter(
            Product.id == product_id,
            Product.tenant_id == tenant_id
        ).first()

    @staticmethod
    def delete(db: Session, product_id: UUID, tenant_id: UUID):
        product = ProductRepository.get_by_id(db, product_id, tenant_id)
        if product:
            db.delete(product)
            db.commit()
            return True
        return False
