from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from infrastructure.db.session import get_db
from src.repositories.product_repository import ProductRepository
from domains.product.model import Product
from pydantic import BaseModel

router = APIRouter(prefix="/products", tags=["products"])

class ProductCreate(BaseModel):
    name: str
    sku: str
    price: float

@router.post("/")
def create_product(product_data: ProductCreate, request: Request, db: Session = Depends(get_db)):
    tenant_id = request.state.tenant_id
    new_product = Product(
        tenant_id=tenant_id,
        name=product_data.name,
        sku=product_data.sku,
        price=product_data.price
    )
    return ProductRepository.create(db, new_product)

@router.get("/")
def get_products(request: Request, db: Session = Depends(get_db)):
    tenant_id = request.state.tenant_id
    return ProductRepository.get_all_by_tenant(db, UUID(tenant_id))
