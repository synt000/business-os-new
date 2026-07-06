from sqlalchemy.orm import Session
from domains.product.product_model import Product

class ProductRepository:

    @staticmethod
    def create(db: Session, product: Product):
        db.add(product)
        db.commit()
        db.refresh(product)
        return product

    @staticmethod
    def list(db: Session, tenant_id: str):
        return db.query(Product).filter(
            Product.tenant_id == tenant_id
        ).all()
