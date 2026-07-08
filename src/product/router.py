import os
from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

# Authoritative Core Connections Matrix
from ..database import get_db
from ..models.saas_core import User, Product, Order, OrderItem, Category
from ..config.security import get_current_user

router = APIRouter(prefix="/api/v4/business", tags=["Omnichannel Business Engine"])

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

class CategoryCreateInboundSchema(BaseModel):
    name: str

class CategoryUpdateInboundSchema(BaseModel):
    name: str

class OrderItemInboundSchema(BaseModel):
    product_id: str
    quantity: int

class OrderCreateInboundSchema(BaseModel):
    platform_channel: str
    customer_name: str
    customer_phone: Optional[str] = None
    items: List[OrderItemInboundSchema]

# ==========================================================================
# 1. CATEGORIES COMPLETE CRUD PIPELINES (WITH MULTI-TENANT ISOLATION)
# ==========================================================================
@router.post("/categories", status_code=status.HTTP_201_CREATED)
async def create_isolated_category(payload: CategoryCreateInboundSchema, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not payload.name.strip():
        raise HTTPException(status_code=422, detail="Category name cannot be empty")
    new_cat = Category(name=payload.name, tenant_id=current_user.tenant_id)
    db.add(new_cat)
    db.commit()
    return {"status": "CATEGORY_CREATED", "tenant_id": current_user.tenant_id}

@router.get("/categories")
async def fetch_isolated_categories(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    cats = db.query(Category).filter(Category.tenant_id == current_user.tenant_id).all()
    return {"categories": [{"id": c.id, "name": c.name} for c in cats]}

@router.put("/categories/{category_id}")
async def update_isolated_category(category_id: int, payload: CategoryUpdateInboundSchema, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not payload.name.strip():
        raise HTTPException(status_code=422, detail="Category name cannot be empty")
    target_cat = db.query(Category).filter(Category.id == category_id, Category.tenant_id == current_user.tenant_id).first()
    if not target_cat:
        raise HTTPException(status_code=404, detail="CATEGORY_NOT_FOUND_IN_THIS_WORKSPACE")
    target_cat.name = payload.name
    db.commit()
    return {"status": "CATEGORY_SUCCESSFULLY_UPDATED", "category_id": category_id}

@router.delete("/categories/{category_id}")
async def delete_isolated_category(category_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    target_cat = db.query(Category).filter(Category.id == category_id, Category.tenant_id == current_user.tenant_id).first()
    if not target_cat:
        raise HTTPException(status_code=404, detail="CATEGORY_NOT_FOUND_IN_THIS_WORKSPACE")
    db.delete(target_cat)
    db.commit()
    return {"status": "CATEGORY_SUCCESSFULLY_DELETED", "category_id": category_id}

# ==========================================================================
# 2. CORE PRODUCTS CRUD PIPELINES MATRIX
# ==========================================================================
@router.post("/products", status_code=status.HTTP_201_CREATED)
async def create_isolated_product_item(payload: ProductCreateInboundSchema, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not payload.name.strip() or not payload.sku.strip():
        raise HTTPException(status_code=422, detail="VALIDATION_ERROR: NAME_AND_SKU_ARE_REQUIRED")
    duplicate_sku = db.query(Product).filter(Product.sku == payload.sku, Product.tenant_id == current_user.tenant_id).first()
    if duplicate_sku:
        raise HTTPException(status_code=400, detail="CONFLICT: SKU_ALREADY_EXISTS_IN_THIS_WORKSPACE")
    product_id = f"prd_{int(datetime.utcnow().timestamp())}"
    new_product = Product(id=product_id, name=payload.name, sku=payload.sku, barcode=payload.barcode, stock_qty=payload.stock_qty, purchase_price=payload.purchase_price, retail_price=payload.retail_price, tenant_id=current_user.tenant_id)
    db.add(new_product)
    db.commit()
    return {"status": "PRODUCT_SUCCESSFULLY_CREATED", "product_id": product_id}

@router.get("/products")
async def fetch_all_isolated_products(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    tenant_products = db.query(Product).filter(Product.tenant_id == current_user.tenant_id).all()
    return {"tenant_id": current_user.tenant_id, "total_items": len(tenant_products), "products": [{"id": p.id, "name": p.name, "sku": p.sku, "barcode": p.barcode, "stock_qty": p.stock_qty, "purchase_price": p.purchase_price, "retail_price": p.retail_price} for p in tenant_products]}

@router.put("/products/{product_id}")
async def update_isolated_product_item(product_id: str, payload: ProductUpdateInboundSchema, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    target_product = db.query(Product).filter(Product.id == product_id, Product.tenant_id == current_user.tenant_id).first()
    if not target_product:
        raise HTTPException(status_code=404, detail="PRODUCT_NOT_FOUND_IN_THIS_WORKSPACE")
    update_data = payload.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(target_product, key, value)
    db.commit()
    return {"status": "PRODUCT_SUCCESSFULLY_UPDATED", "product_id": product_id}

@router.delete("/products/{product_id}")
async def delete_isolated_product_item(product_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    target_product = db.query(Product).filter(Product.id == product_id, Product.tenant_id == current_user.tenant_id).first()
    if not target_product:
        raise HTTPException(status_code=404, detail="PRODUCT_NOT_FOUND_IN_THIS_WORKSPACE")
    db.delete(target_product)
    db.commit()
    return {"status": "PRODUCT_SUCCESSFULLY_DELETED", "product_id": product_id}

# ==========================================================================
# 3. PRODUCTION REALTIME ISOLATED ORDERS OPERATIONS (INVENTORY DEDUCTION)
# ==========================================================================
@router.post("/orders", status_code=status.HTTP_201_CREATED)
async def ingest_isolated_omnichannel_order(payload: OrderCreateInboundSchema, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not payload.customer_name.strip() or not payload.items:
        raise HTTPException(status_code=422, detail="VALIDATION_ERROR: CUSTOMER_NAME_AND_ITEMS_ARE_REQUIRED")
        
    order_id = f"ord_{int(datetime.utcnow().timestamp())}"
    order_num = f"ORD-{datetime.utcnow().strftime('%Y%m%d')}-{int(datetime.utcnow().timestamp()) % 10000:04d}"
    
    new_order = Order(
        id=order_id, order_number=order_num, platform_channel=payload.platform_channel,
        customer_name=payload.customer_name, customer_phone=payload.customer_phone,
        total_amount=0.0, order_status="PENDING", tenant_id=current_user.tenant_id
    )
    db.add(new_order)
    computed_total_pool = 0.0
    
    for item in payload.items:
        target_product = db.query(Product).filter(Product.id == item.product_id, Product.tenant_id == current_user.tenant_id).first()
        if not target_product:
            raise HTTPException(status_code=404, detail=f"PRODUCT_ID_{item.product_id}_NOT_FOUND_IN_THIS_WORKSPACE")
        if target_product.stock_qty < item.quantity:
            raise HTTPException(status_code=400, detail=f"INSUFFICIENT_STOCK: {target_product.name} has only {target_product.stock_qty} units left")
            
        # Automated inventory pool deduction guards
        target_product.stock_qty -= item.quantity
        sale_price = target_product.retail_price
        computed_total_pool += (sale_price * item.quantity)
        
        new_item = OrderItem(quantity=item.quantity, price_at_sale=sale_price, order_id=order_id, product_id=target_product.id)
        db.add(new_item)
        
    new_order.total_amount = computed_total_pool
    try:
        db.commit()
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"TRANSACTION_FAILED: {str(exc)}")
    return {"status": "ORDER_SUCCESSFULLY_SYNCED", "order_id": order_id, "order_number": order_num, "total_amount": computed_total_pool}

@router.get("/orders")
async def fetch_all_isolated_orders(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    tenant_orders = db.query(Order).filter(Order.tenant_id == current_user.tenant_id).order_by(Order.created_at.desc()).all()
    return {
        "tenant_id": current_user.tenant_id,
        "total_orders": len(tenant_orders),
        "orders": [
            {
                "id": o.id, "order_number": o.order_number, "platform": o.platform_channel,
                "customer": o.customer_name, "phone": o.customer_phone, "total_usd": o.total_amount,
                "status": o.order_status, "created_at": o.created_at
            } for o in tenant_orders
        ]
    }
