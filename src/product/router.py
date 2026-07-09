import os
from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import func

# Authoritative Core Connections Matrix
from ..database import get_db
from ..models.saas_core import User, Product, Order, OrderItem, Category, AuditLog, AccountLedger
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

def log_security_audit_action(db: Session, user_id: str, tenant_id: str, action: str, module: str, details: str, request: Request = None):
    client_ip = "127.0.0.1"
    if request and request.client:
        client_ip = request.client.host
    audit_entry = AuditLog(action_type=action, module_name=module, details_log=details, ip_address=client_ip, user_id=user_id, tenant_id=tenant_id)
    db.add(audit_entry)

def record_double_entry_accounting(db: Session, tenant_id: str, entry_type: str, account_head: str, amount: float, reference_id: str, description: str):
    ledger_id = f"ldg_{entry_type[:3].lower()}_{int(datetime.utcnow().timestamp())}_{reference_id[-4:]}"
    ledger_entry = AccountLedger(id=ledger_id, entry_type=entry_type, account_head=account_head, amount=amount, reference_id=reference_id, description=description, tenant_id=tenant_id)
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
    db.commit()
    return {"status": "PRODUCT_SUCCESSFULLY_CREATED", "product_id": product_id}

@router.get("/products")
async def fetch_all_isolated_products(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    tenant_products = db.query(Product).filter(Product.tenant_id == current_user.tenant_id).all()
    return {"tenant_id": current_user.tenant_id, "total_items": len(tenant_products), "products": [{"id": p.id, "name": p.name, "sku": p.sku, "barcode": p.barcode, "stock_qty": p.stock_qty, "purchase_price": p.purchase_price, "retail_price": p.retail_price} for p in tenant_products]}

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
# 3. PRODUCTION AUTOMATED ACCOUNTING DOUBLE-ENTRY ORDERS INGESTION
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
    computed_cogs_pool = 0.0
    
    for item in payload.items:
        target_product = db.query(Product).filter(Product.id == item.product_id, Product.tenant_id == current_user.tenant_id).first()
        if not target_product:
            raise HTTPException(status_code=404, detail=f"PRODUCT_ID_{item.product_id}_NOT_FOUND_IN_THIS_WORKSPACE")
        if target_product.stock_qty < item.quantity:
            raise HTTPException(status_code=400, detail=f"INSUFFICIENT_STOCK: {target_product.name} has only {target_product.stock_qty} units left")
            
        target_product.stock_qty -= item.quantity
        sale_price = target_product.retail_price
        cogs_price = target_product.purchase_price
        
        computed_total_pool += (sale_price * item.quantity)
        computed_cogs_pool += (cogs_price * item.quantity)
        
        new_item = OrderItem(quantity=item.quantity, price_at_sale=sale_price, order_id=order_id, product_id=target_product.id)
        db.add(new_item)
        
    new_order.total_amount = computed_total_pool
    
    # 1. Increase Cash/Receivable Asset (DEBIT) and Increase Sales Revenue (CREDIT)
    record_double_entry_accounting(db, current_user.tenant_id, "DEBIT", "CASH_ASSET", computed_total_pool, order_id, f"Inbound cash received from sales invoice {order_num}")
    record_double_entry_accounting(db, current_user.tenant_id, "CREDIT", "SALES_REVENUE", computed_total_pool, order_id, f"Recognized revenue earned from order {order_num}")
    
    # 2. Increase Cost of Goods Sold Expense (DEBIT) and Decrease Inventory Asset (CREDIT)
    record_double_entry_accounting(db, current_user.tenant_id, "DEBIT", "COGS_EXPENSE", computed_cogs_pool, order_id, f"Cost of goods sold recorded for invoice {order_num}")
    record_double_entry_accounting(db, current_user.tenant_id, "CREDIT", "INVENTORY_ASSET", computed_cogs_pool, order_id, f"Asset inventory reduction mapped from sales checkout {order_num}")
    
    # Write Audit Trail Telemetry
    log_security_audit_action(db, current_user.id, current_user.tenant_id, "CREATE", "ORDERS", f"Processed invoice {order_num} and triggered automated accounting matrixes", request)
    
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

# ==========================================================================
# MASTER PROMPT V5.0 NEW API: ISOLATED P&L PROFIT & LOSS STATEMENT REPORT
# ==========================================================================
@router.get("/accounting/profit-loss")
async def generate_isolated_profit_loss_statement(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Computes pure accrual accounting outputs extracting isolated revenues, expenses, and net profit margins."""
    total_revenue = db.query(func.sum(AccountLedger.amount)).filter(AccountLedger.tenant_id == current_user.tenant_id, AccountLedger.account_head == "SALES_REVENUE").scalar() or 0.0
    total_cogs = db.query(func.sum(AccountLedger.amount)).filter(AccountLedger.tenant_id == current_user.tenant_id, AccountLedger.account_head == "COGS_EXPENSE").scalar() or 0.0
    
    gross_profit = total_revenue - total_cogs
    net_profit = gross_profit
    profit_margin_pct = (net_profit / total_revenue * 100) if total_revenue > 0 else 0.0
    
    return {
        "tenant_id": current_user.tenant_id,
        "report_type": "ACCRUAL_PROFIT_AND_LOSS_STATEMENT",
        "generated_at": datetime.utcnow(),
        "financial_summary": {
            "total_gross_revenue": total_revenue,
            "total_cost_of_goods_sold": total_cogs,
            "gross_profit_margin": gross_profit,
            "net_operational_profit": net_profit,
            "net_profit_margin_percentage": f"{profit_margin_pct:.2f}%"
        }
    }
