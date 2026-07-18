from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database import get_db
from . import service
from .schemas import TenantStatusUpdate


router = APIRouter(
    prefix="/admin",
    tags=["Admin SaaS"]
)


@router.get("/health")
def admin_health():
    return {
        "module": "admin",
        "status": "ready"
    }


@router.get("/tenants")
def tenants(db: Session = Depends(get_db)):
    data = service.list_tenants(db)

    return [
        {
            "id": t.id,
            "company_name": t.company_name,
            "owner_email": t.owner_email,
            "subscription_tier": t.subscription_tier,
            "billing_active": t.is_billing_active
        }
        for t in data
    ]


@router.get("/tenants/{tenant_id}")
def tenant_detail(
    tenant_id: str,
    db: Session = Depends(get_db)
):
    tenant = service.get_tenant(db, tenant_id)

    if not tenant:
        raise HTTPException(
            status_code=404,
            detail="Tenant not found"
        )

    return {
        "id": tenant.id,
        "company_name": tenant.company_name,
        "owner_email": tenant.owner_email,
        "subscription_tier": tenant.subscription_tier,
        "billing_active": tenant.is_billing_active
    }


@router.post("/tenants/{tenant_id}/billing")
def billing_update(
    tenant_id: str,
    payload: TenantStatusUpdate,
    db: Session = Depends(get_db)
):
    tenant = service.update_billing_status(
        db,
        tenant_id,
        payload.is_billing_active
    )

    if not tenant:
        raise HTTPException(
            status_code=404,
            detail="Tenant not found"
        )

    return {
        "status": "updated",
        "tenant_id": tenant.id,
        "billing_active": tenant.is_billing_active
    }
