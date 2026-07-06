from domains.product.category_model import Category
from repositories.category_repository import CategoryRepository

class CategoryService:

    @staticmethod
    def create(db, name: str, description: str, tenant_id: str):

        category = Category(
            name=name,
            description=description,
            tenant_id=tenant_id
        )

        return CategoryRepository.create(db, category)

    @staticmethod
    def list(db, tenant_id: str):
        return CategoryRepository.list(db, tenant_id)
