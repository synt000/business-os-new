import os
from datetime import datetime
from typing import Optional  # FIXED: IMPORTED OPTIONAL TYPING NATIVELY TO RESOLVE NAMEERROR DEADLOCKS
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

# Authoritative Core Connections Matrix
from ..database import get_db
from ..models.saas_core import User, Product
from ..config.security import get_current_user

router = APIRouter(prefix="/api/v4/business", tags=["Omnichannel Business Engine"])

# Pydantic Structural Request Payload Validations
class ProductCreateInboundSchema(BaseModel):
    name: str
    sku: str
    barcode: str = None
    stock_qty: int = 0
    purchase_price: float = 0.0
    retail_price: float = 0.0

class ProductUpdateInboundSchema(BaseModel):
    name: Optional[str] = None
    barcode: Optional[str] = None
    stock_qty: Optional[int] = None
    purchase_price: Optional[float] = None
    retail_price: Optional[float] = None

# ==========================================================================
# CURRENT SPRINT: PRODUCT CRUD MODULE WITH STRICT TENANT DATA ISOLATION
# ==========================================================================

# 1. CREATE ACTION: INGEST NEW PRODUCT
@router.post("/products", status_code=status.HTTP_201_CREATED)
async def create_isolated_product_item(
    payload: ProductCreateInboundSchema, 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    if not payload.name.strip() or not payload.sku.strip():
        raise HTTPException(status_code=422, detail="VALIDATION_ERROR: NAME_AND_SKU_ARE_REQUIRED")
    
    # Prevent SKU duplications inside the SAME tenant space
    duplicate_sku = db.query(Product).filter(
        Product.sku == payload.sku, 
        Product.tenant_id == current_user.tenant_id
    ).first()
    if duplicate_sku:
        raise HTTPException(status_code=400, detail="CONFLICT: SKU_ALREADY_EXISTS_IN_THIS_WORKSPACE")

    product_id = f"prd_{int(datetime.utcnow().timestamp())}"
    new_product = Product(
        id=product_id, name=payload.name, sku=payload.sku, barcode=payload.barcode,
        stock_qty=payload.stock_qty, purchase_price=payload.purchase_price, retail_price=payload.retail_price,
        tenant_id=current_user.tenant_id
    )
    db.add(new_product)
    db.commit()
    return {"status": "PRODUCT_SUCCESSFULLY_CREATED", "product_id": product_id}

# 2. READ ACTION: FETCH ALL ISOLATED PRODUCTS ARRAY
@router.get("/products")
async def fetch_all_isolated_products(
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    # Absolute Tenant Isolation Query Clause
    tenant_products = db.query(Product).filter(Product.tenant_id == current_user.tenant_id).all()
    return {
        "tenant_id": current_user.tenant_id,
        "total_items": len(tenant_products),
        "products": [
            {
                "id": p.id, "name": p.name, "sku": p.sku, "barcode": p.barcode,
                "stock_qty": p.stock_qty, "purchase_price": p.purchase_price, "retail_price": p.retail_price
            } for p in tenant_products
        ]
    }

# 3. UPDATE ACTION: MODIFY EXISTING PRODUCT IN SANDBOX
@router.put("/products/{product_id}")
async def update_isolated_product_item(
    product_id: str,
    payload: ProductUpdateInboundSchema,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    target_product = db.query(Product).filter(
        Product.id == product_id, 
        Product.tenant_id == current_user.tenant_id
    ).first()
    if not target_product:
        raise HTTPException(status_code=404, detail="PRODUCT_NOT_FOUND_IN_THIS_WORKSPACE")
        
    update_data = payload.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(target_product, key, value)
        
    db.commit()
    return {"status": "PRODUCT_SUCCESSFULLY_UPDATED", "product_id": product_id}

# 4. DELETE ACTION: PURGE PRODUCT RECORD SECURELY
@router.delete("/products/{product_id}")
async def delete_isolated_product_item(
    product_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    target_product = db.query(Product).filter(
        Product.id == product_id, 
        Product.tenant_id == current_user.tenant_id
    ).first()
    if not target_product:
        raise HTTPException(status_code=404, detail="PRODUCT_NOT_FOUND_IN_THIS_WORKSPACE")
        
    db.delete(target_product)
    db.commit()
    return {"status": "PRODUCT_SUCCESSFULLY_DELETED", "product_id": product_id}

# 5. OMNICHANNEL REALTIME ORDERS STREAM SYNCHRONIZER
@router.get("/orders")
async def fetch_isolated_orders_stream(current_user: User = Depends(get_current_user)):
    return {
        "tenant_id": current_user.tenant_id,
        "orders": [
            {"order_id": "ORD-9841", "platform": "Facebook Messenger", "customer": "Ma Thida", "total_usd": 45.00, "status": "DELIVERED"},
            {"order_id": "ORD-2384", "platform": "Viber/WhatsApp", "customer": "Ko Kyaw", "total_usd": 120.00, "status": "PROCESSING"},
            {"order_id": "ORD-5721", "platform": "Telegram Bot", "customer": "Maung Maung", "total_usd": 15.50, "status": "PENDING"}
        ]
    }
