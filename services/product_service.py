from domains.product.product_model import Product
from repositories.product_repository import ProductRepository

class ProductService:

    @staticmethod
    def create(db, name: str, price: float, category_id: str, tenant_id: str):

        product = Product(
            name=name,
            price=price,
            category_id=category_id,
            tenant_id=tenant_id
        )

        return ProductRepository.create(db, product)

    @staticmethod
    def list(db, tenant_id: str):
        return ProductRepository.list(db, tenant_id)
