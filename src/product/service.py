from sqlalchemy.orm import Session
from uuid import UUID
from src.product.repository import ProductRepository
from src.product.schemas import ProductCreate, ProductUpdate
from fastapi import HTTPException, status

class ProductService:
    def __init__(self, db: Session):
        self.repository = ProductRepository(db)

    def create_product(self, tenant_id: UUID, product_data: ProductCreate):
        if self.repository.get_by_sku(product_data.sku, tenant_id):
            raise HTTPException(status_code=400, detail="SKU already exists")
        
        data = product_data.dict()
        data["tenant_id"] = tenant_id
        return self.repository.create(data)

    def get_products(self, tenant_id: UUID):
        return self.repository.get_all(tenant_id)

    def get_product(self, product_id: UUID, tenant_id: UUID):
        product = self.repository.get_by_id(product_id, tenant_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product

    def update_product(self, product_id: UUID, tenant_id: UUID, product_data: ProductUpdate):
        product = self.get_product(product_id, tenant_id)
        return self.repository.update(product, product_data.dict(exclude_unset=True))

    def delete_product(self, product_id: UUID, tenant_id: UUID):
        product = self.get_product(product_id, tenant_id)
        self.repository.delete(product)
        return {"detail": "Product deleted successfully"}
