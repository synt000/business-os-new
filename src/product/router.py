import os
from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session

# Authoritative Core Connections Matrix
from ..database import get_db
from ..models.saas_core import User, Product, Order, OrderItem, Category, AuditLog, InventoryLedger
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

class StockAdjustmentInboundSchema(BaseModel):
    product_id: str
    transaction_type: str
    quantity_changed: int
    reason_note: Optional[str] = None

def log_security_audit_action(db: Session, user_id: str, tenant_id: str, action: str, module: str, details: str, request: Request = None):
    client_ip = "127.0.0.1"
    if request and request.client:
        client_ip = request.client.host
    audit_entry = AuditLog(action_type=action, module_name=module, details_log=details, ip_address=client_ip, user_id=user_id, tenant_id=tenant_id)
    db.add(audit_entry)

def write_inventory_ledger_transaction(db: Session, user_id: str, tenant_id: str, product_id: str, tx_type: str, qty_changed: int, prev_stock: int, curr_stock: int, note: str = None):
    ledger_entry = InventoryLedger(transaction_type=tx_type, quantity_changed=qty_changed, previous_stock=prev_stock, current_stock=curr_stock, reason_note=note, product_id=product_id, user_id=user_id, tenant_id=tenant_id)
    db.add(ledger_entry)

# ==========================================================================
# 1. CATEGORIES COMPLETE CRUD PIPELINES (WITH INTEGRATED TELEMETRY)
# ==========================================================================
@router.post("/categories", status_code=status.HTTP_201_CREATED)
async def create_isolated_category(payload: CategoryCreateInboundSchema, request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not payload.name.strip():
        raise HTTPException(status_code=422, detail="Category name cannot be empty")
    new_cat = Category(name=payload.name, tenant_id=current_user.tenant_id)
    db.add(new_cat)
    log_security_audit_action(db, current_user.id, current_user.tenant_id, "CREATE", "CATEGORIES", f"Created category: {payload.name}", request)
    db.commit()
    return {"status": "CATEGORY_CREATED", "tenant_id": current_user.tenant_id}

@router.get("/categories")
async def fetch_isolated_categories(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    cats = db.query(Category).filter(Category.tenant_id == current_user.tenant_id).all()
    return {"categories": [{"id": c.id, "name": c.name} for c in cats]}

@router.put("/categories/{category_id}")
async def update_isolated_category(category_id: int, payload: CategoryUpdateInboundSchema, request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not payload.name.strip():
        raise HTTPException(status_code=422, detail="Category name cannot be empty")
    target_cat = db.query(Category).filter(Category.id == category_id, Category.tenant_id == current_user.tenant_id).first()
    if not target_cat:
        raise HTTPException(status_code=404, detail="CATEGORY_NOT_FOUND_IN_THIS_WORKSPACE")
    old_name = target_cat.name
    target_cat.name = payload.name
    log_security_audit_action(db, current_user.id, current_user.tenant_id, "UPDATE", "CATEGORIES", f"Updated category ID {category_id} from '{old_name}' to '{payload.name}'", request)
    db.commit()
    return {"status": "CATEGORY_SUCCESSFULLY_UPDATED", "category_id": category_id}

@router.delete("/categories/{category_id}")
async def delete_isolated_category(category_id: int, request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    target_cat = db.query(Category).filter(Category.id == category_id, Category.tenant_id == current_user.tenant_id).first()
    if not target_cat:
        raise HTTPException(status_code=404, detail="CATEGORY_NOT_FOUND_IN_THIS_WORKSPACE")
    log_security_audit_action(db, current_user.id, current_user.tenant_id, "DELETE", "CATEGORIES", f"Purged category: {target_cat.name} (ID: {category_id})", request)
    db.delete(target_cat)
    db.commit()
    return {"status": "CATEGORY_SUCCESSFULLY_DELETED", "category_id": category_id}

# ==========================================================================
# 2. CORE PRODUCTS CRUD PIPELINES MATRIX (WITH INTEGRATED TELEMETRY)
# ==========================================================================
@router.post("/products", status_code=status.HTTP_201_CREATED)
async def create_isolated_product_item(payload: ProductCreateInboundSchema, request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not payload.name.strip() or not payload.sku.strip():
        raise HTTPException(status_code=422, detail="VALIDATION_ERROR: NAME_AND_SKU_ARE_REQUIRED")
    duplicate_sku = db.query(Product).filter(Product.sku == payload.sku, Product.tenant_id == current_user.tenant_id).first()
    if duplicate_sku:
        raise HTTPException(status_code=400, detail="CONFLICT: SKU_ALREADY_EXISTS_IN_THIS_WORKSPACE")
    product_id = f"prd_{int(datetime.utcnow().timestamp())}"
    new_product = Product(id=product_id, name=payload.name, sku=payload.sku, barcode=payload.barcode, stock_qty=payload.stock_qty, purchase_price=payload.purchase_price, retail_price=payload.retail_price, tenant_id=current_user.tenant_id)
    db.add(new_product)
    log_security_audit_action(db, current_user.id, current_user.tenant_id, "CREATE", "PRODUCTS", f"Ingested SKU {payload.sku}: {payload.name} with {payload.stock_qty} units", request)
    write_inventory_ledger_transaction(db, current_user.id, current_user.tenant_id, product_id, "STOCK_IN", payload.stock_qty, 0, payload.stock_qty, "Initial Sandbox Inventory Ingestion")
    db.commit()
    return {"status": "PRODUCT_SUCCESSFULLY_CREATED", "product_id": product_id}

@router.get("/products")
async def fetch_all_isolated_products(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    tenant_products = db.query(Product).filter(Product.tenant_id == current_user.tenant_id).all()
    return {"tenant_id": current_user.tenant_id, "total_items": len(tenant_products), "products": [Brief_prd for p in tenant_products for Brief_prd in [{"id": p.id, "name": p.name, "sku": p.sku, "barcode": p.barcode, "stock_qty": p.stock_qty, "purchase_price": p.purchase_price, "retail_price": p.retail_price}]]}

@router.put("/products/{product_id}")
async def update_isolated_product_item(product_id: str, payload: ProductUpdateInboundSchema, request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    target_product = db.query(Product).filter(Product.id == product_id, Product.tenant_id == current_user.tenant_id).first()
    if not target_product:
        raise HTTPException(status_code=404, detail="PRODUCT_NOT_FOUND_IN_THIS_WORKSPACE")
    update_data = payload.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(target_product, key, value)
    log_security_audit_action(db, current_user.id, current_user.tenant_id, "UPDATE", "PRODUCTS", f"Modified item fields for product ID {product_id}", request)
    db.commit()
    return {"status": "PRODUCT_SUCCESSFULLY_UPDATED", "product_id": product_id}

@router.delete("/products/{product_id}")
async def delete_isolated_product_item(product_id: str, request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    target_product = db.query(Product).filter(Product.id == product_id, Product.tenant_id == current_user.tenant_id).first()
    if not target_product:
        raise HTTPException(status_code=404, detail="PRODUCT_NOT_FOUND_IN_THIS_WORKSPACE")
    log_security_audit_action(db, current_user.id, current_user.tenant_id, "DELETE", "PRODUCTS", f"Purged SKU record {target_product.sku}: {target_product.name}", request)
    db.delete(target_product)
    db.commit()
    return {"status": "PRODUCT_SUCCESSFULLY_DELETED", "product_id": product_id}

# ==========================================================================
# 3. PRODUCTION REALTIME ISOLATED ORDERS OPERATIONS (INVENTORY DEDUCTION)
# ==========================================================================
@router.post("/orders", status_code=status.HTTP_201_CREATED)
async def ingest_isolated_omnichannel_order(payload: OrderCreateInboundSchema, request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
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
            
        prev_stock = target_product.stock_qty
        target_product.stock_qty -= item.quantity
        curr_stock = target_product.stock_qty
        sale_price = target_product.retail_price
        computed_total_pool += (sale_price * item.quantity)
        
        new_item = OrderItem(quantity=item.quantity, price_at_sale=sale_price, order_id=order_id, product_id=target_product.id)
        db.add(new_item)
        
        # Write Automated Transactional Inventory Ledger
        write_inventory_ledger_transaction(db, current_user.id, current_user.tenant_id, target_product.id, "ORDER_SALE", -item.quantity, prev_stock, curr_stock, f"Omnichannel Order Ingress Sale: {order_num}")
        
    new_order.total_amount = computed_total_pool
    log_security_audit_action(db, current_user.id, current_user.tenant_id, "CREATE", "ORDERS", f"Processed invoice {order_num} via {payload.platform_channel} for {payload.customer_name}", request)
    try:
        db.commit()
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"TRANSACTION_FAILED: {str(exc)}")
    return {"status": "ORDER_SUCCESSFULLY_SYNCED", "order_id": order_id, "order_number": order_num, "total_amount": computed_total_pool}

@router.get("/orders")
async def fetch_all_isolated_orders(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    tenant_orders = db.query(Order).filter(Order.tenant_id == current_user.tenant_id).order_by(Order.created_at.desc()).all()
    return {"tenant_id": current_user.tenant_id, "total_orders": len(tenant_orders), "orders": [{"id": o.id, "order_number": o.order_number, "platform": o.platform_channel, "customer": o.customer_name, "phone": o.customer_phone, "total_usd": o.total_amount, "status": o.order_status, "created_at": o.created_at} for o in tenant_orders]}

# ==========================================================================
# 4. PRODUCTION NEW API: ADVANCED INVENTORY LEDGER STOCK ADJUSTMENT & LOGS
# ==========================================================================
@router.post("/inventory/stock-adjustment")
async def execute_warehouse_stock_adjustment(payload: StockAdjustmentInboundSchema, request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if payload.transaction_type not in ["STOCK_IN", "STOCK_OUT", "ADJUSTMENT", "DAMAGED"]:
        raise HTTPException(status_code=400, detail="INVALID_TRANSACTION_TYPE_SPECIFICATION")
    if payload.quantity_changed <= 0:
         raise HTTPException(status_code=422, detail="QUANTITY_CHANGED_MUST_BE_A_POSITIVE_INTEGER")
         
    target_product = db.query(Product).filter(Product.id == payload.product_id, Product.tenant_id == current_user.tenant_id).first()
    if not target_product:
        raise HTTPException(status_code=404, detail="PRODUCT_NOT_FOUND_IN_THIS_WORKSPACE")
        
    prev_stock = target_product.stock_qty
    
    if payload.transaction_type in ["STOCK_IN"]:
        target_product.stock_qty += payload.quantity_changed
        net_qty = payload.quantity_changed
    else:
        if target_product.stock_qty < payload.quantity_changed:
            raise HTTPException(status_code=400, detail=f"INSUFFICIENT_STOCK: Workspace contains only {target_product.stock_qty} units")
        target_product.stock_qty -= payload.quantity_changed
        net_qty = -payload.quantity_changed
        
    curr_stock = target_product.stock_qty
    
    write_inventory_ledger_transaction(db, current_user.id, current_user.tenant_id, target_product.id, payload.transaction_type, net_qty, prev_stock, curr_stock, payload.reason_note)
    log_security_audit_action(db, current_user.id, current_user.tenant_id, "UPDATE", "INVENTORY", f"Executed warehouse {payload.transaction_type} adjustments for SKU {target_product.sku}", request)
    
    try:
        db.commit()
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"INVENTORY_TRANSACTION_FAILED: {str(exc)}")
        
    return {"status": "INVENTORY_LEDGER_ADJUSTMENT_SUCCESSFUL", "product_id": payload.product_id, "previous_stock": prev_stock, "current_stock": curr_stock}

@router.get("/inventory/ledgers")
async def fetch_tenant_inventory_ledger_history(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    ledger_logs = db.query(InventoryLedger).filter(InventoryLedger.tenant_id == current_user.tenant_id).order_by(InventoryLedger.created_at.desc()).all()
    return {"tenant_id": current_user.tenant_id, "total_log_records": len(ledger_logs), "ledgers": [{"id": l.id, "product_id": l.product_id, "tx_type": l.transaction_type, "quantity_changed": l.quantity_changed, "previous_stock": l.previous_stock, "current_stock": l.current_stock, "note": l.reason_note, "timestamp": l.created_at} for l in ledger_logs]}
