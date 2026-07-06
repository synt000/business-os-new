from sqlalchemy.orm import Session
from domains.product.model import Product
from domains.category.model import Category
from domains.movement.model import Movement
from uuid import UUID

class DashboardService:
    @staticmethod
    def get_summary(db: Session, tenant_id: UUID):
        product_count = db.query(Product).filter(Product.tenant_id == tenant_id).count()
        category_count = db.query(Category).filter(Category.tenant_id == tenant_id).count()
        recent_movements = db.query(Movement).filter(Movement.tenant_id == tenant_id).order_by(Movement.created_at.desc()).limit(5).all()
        
        return {
            "product_count": product_count,
            "category_count": category_count,
            "recent_movements": recent_movements
        }
