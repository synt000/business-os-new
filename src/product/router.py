from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session
from src.database import SessionLocal
from src.product.schemas import ProductCreate, ProductUpdate, ProductResponse
from src.product.service import ProductService
from typing import List
from uuid import UUID

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

router = APIRouter(prefix="/products", tags=["products"])

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(request: Request, product: ProductCreate, db: Session = Depends(get_db)):
    return ProductService(db).create_product(request.state.tenant_id, product)

@router.get("/", response_model=List[ProductResponse])
def list_products(request: Request, db: Session = Depends(get_db)):
    return ProductService(db).get_products(request.state.tenant_id)

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(request: Request, product_id: UUID, db: Session = Depends(get_db)):
    return ProductService(db).get_product(product_id, request.state.tenant_id)

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(request: Request, product_id: UUID, product: ProductUpdate, db: Session = Depends(get_db)):
    return ProductService(db).update_product(product_id, request.state.tenant_id, product)

@router.delete("/{product_id}")
def delete_product(request: Request, product_id: UUID, db: Session = Depends(get_db)):
    return ProductService(db).delete_product(product_id, request.state.tenant_id)
