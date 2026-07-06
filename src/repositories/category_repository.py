from sqlalchemy.orm import Session
from domains.category.model import Category
from uuid import UUID

class CategoryRepository:
    @staticmethod
    def create(db: Session, category: Category):
        db.add(category)
        db.commit()
        db.refresh(category)
        return category

    @staticmethod
    def get_all_by_tenant(db: Session, tenant_id: UUID):
        return db.query(Category).filter(Category.tenant_id == tenant_id).all()
