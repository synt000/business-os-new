from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.database_mega_upgrade import FranchiseNetwork
from src.domains.inventory.models import Inventory

router = APIRouter(prefix="/franchise", tags=["Franchise Enterprise Network"])

@router.post("/register-branch")
def link_branch_node(hq_id: str, branch_id: str, location_tag: str = "Primary_Branch", db: Session = Depends(get_db)):
    """
    Establish a corporate network architecture linking a subsidiary branch tenant 
    directly to a parent Headquarter (HQ) workspace context node.
    """
    # Verify if the branch is already linked to any network structure
    existing_link = db.query(FranchiseNetwork).filter(FranchiseNetwork.branch_tenant_id == branch_id).first()
    if existing_link:
        raise HTTPException(status_code=400, detail="This branch workspace node is already registered inside a network.")
        
    network_node = FranchiseNetwork(
        headquarter_tenant_id=hq_id,
        branch_tenant_id=branch_id,
        branch_location_tag=location_tag,
        is_active=True
    )
    db.add(network_node)
    db.commit()
    db.refresh(network_node)
    return {"status": "success", "message": "✓ Corporate Franchise Link Enforced.", "node_id": network_node.id}

@router.get("/hq-monitor/{hq_id}")
def monitor_network_inventory(hq_id: str, db: Session = Depends(get_db)):
    """
    Aggregated Headquarter Monitoring Engine: Fetches real-time consolidated stock levels 
    across all active branch network workspace tenants.
    """
    branches = db.query(FranchiseNetwork).filter(
        FranchiseNetwork.headquarter_tenant_id == hq_id,
        FranchiseNetwork.is_active == True
    ).all()
    
    aggregated_report = []
    for branch in branches:
        # Cross-query inventory table using isolated branch tenant parameters securely
        branch_stocks = db.query(Inventory).filter(Inventory.tenant_id == branch.branch_tenant_id).all()
        stock_summary = [{"product_id": s.product_id, "quantity": s.quantity} for s in branch_stocks]
        
        aggregated_report.append({
            "branch_tenant_id": branch.branch_tenant_id,
            "location_tag": branch.branch_location_tag,
            "live_stock_matrix": stock_summary
        })
        
    return {
        "headquarter_tenant_id": hq_id,
        "total_active_branches": len(branches),
        "network_consolidated_data": aggregated_report
    }
