import os
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

# Authoritative Connection Mappings
from ..database import get_db
from ..models.saas_core import User, Product
from ..config.security import get_current_user

router = APIRouter(prefix="/api/v4/products", tags=["Core Product Module"])

# Pydantic Product Validation Schema Shards
class ProductCreateInboundSchema(BaseModel):
    name: str
    sku: str
    barcode: str = None
    stock_qty: int = 0
    purchase_price: float = 0.0
    retail_price: float = 0.0

# ==========================================================================
# PHASE 3: CREATE ISOLATED PRODUCT WITH STRICT TENANT_ID INTERCEPTOR
# ==========================================================================
@router.post("", status_code=status.HTTP_201_CREATED)
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
        id=product_id,
        name=payload.name,
        sku=payload.sku,
        barcode=payload.barcode,
        stock_qty=payload.stock_qty,
        purchase_price=payload.purchase_price,
        retail_price=payload.retail_price,
        tenant_id=current_user.tenant_id  # Enforce Absolute Data Privacy
    )
    db.add(new_product)
    
    try:
        db.commit()
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"TRANSACTION_FAILED: {str(exc)}")
        
    return {"status": "PRODUCT_SUCCESSFULLY_CREATED", "product_id": product_id, "tenant_id": current_user.tenant_id}

# ==========================================================================
# PHASE 3: READ / FETCH ALL PRODUCTS ENFORCING RIGID TENANT ISOLATION
# ==========================================================================
@router.get("")
async def fetch_all_isolated_products(
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    # Tenant A can NEVER query Tenant B inventory logs
    tenant_products = db.query(Product).filter(Product.tenant_id == current_user.tenant_id).all()
    
    return {
        "tenant_id": current_user.tenant_id,
        "scope": "TENANT_ISOLATED_DATA_ARRAY",
        "total_items": len(tenant_products),
        "products": [
            {
                "id": p.id, "name": p.name, "sku": p.sku, "barcode": p.barcode,
                "stock_qty": p.stock_qty, "purchase_price": p.purchase_price, "retail_price": p.retail_price,
                "created_at": p.created_at
            } for p in tenant_products
        ]
    }
