from sqlalchemy.orm import Session
from domains.product.category_model import Category

class CategoryRepository:

    @staticmethod
    def create(db: Session, category: Category):
        db.add(category)
        db.commit()
        db.refresh(category)
        return category

    @staticmethod
    def list(db: Session, tenant_id: str):
        return db.query(Category).filter(
            Category.tenant_id == tenant_id
        ).all()
