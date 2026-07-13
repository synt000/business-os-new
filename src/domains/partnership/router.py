from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.database_mega_upgrade import TenantPartnership
from src.domains.product.models import Product
import json

router = APIRouter(prefix="/partnership", tags=["B2B Partnership Engine"])

@router.post("/connect")
def establish_partnership(supplier_id: str, dropshipper_id: str, db: Session = Depends(get_db)):
    """
    Establish a secure B2B network link between a wholesale supplier tenant 
    and a retail dropshipper tenant within the SaaS ecosystem.
    """
    # Check if link already exists
    existing = db.query(TenantPartnership).filter(
        TenantPartnership.supplier_tenant_id == supplier_id,
        TenantPartnership.dropshipper_tenant_id == dropshipper_id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="B2B Partnership link already active on this node.")
        
    partnership = TenantPartnership(
        supplier_tenant_id=supplier_id,
        dropshipper_tenant_id=dropshipper_id,
        status="active",
        shared_sku_footprint=json.dumps([])
    )
    db.add(partnership)
    db.commit()
    db.refresh(partnership)
    return {"status": "success", "message": "✓ B2B Network Connection Established.", "partnership_id": partnership.id}

@router.get("/shared-products/{dropshipper_id}")
def get_shared_catalog(dropshipper_id: str, db: Session = Depends(get_db)):
    """
    Fetch shared wholesale catalogs that this dropshipper tenant has permission 
    to view from connected suppliers.
    """
    links = db.query(TenantPartnership).filter(
        TenantPartnership.dropshipper_tenant_id == dropshipper_id,
        TenantPartnership.status == "active"
    ).all()
    
    catalog = []
    for link in links:
        # Fetch all products belonging to the supplier tenant context
        supplier_products = db.query(Product).filter(Product.tenant_id == link.supplier_tenant_id).all()
        for p in supplier_products:
            catalog.append({
                "product_id": p.id,
                "sku": p.sku,
                "name": p.name,
                "wholesale_price": p.price,
                "supplier_node": link.supplier_tenant_id
            })
            
    return {"dropshipper_tenant_id": dropshipper_id, "available_shared_stock": catalog}
