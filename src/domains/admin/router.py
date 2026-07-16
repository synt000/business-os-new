from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database import get_db
from src.domains.admin.service import (
    list_tenants,
    get_tenant,
    update_billing_status
)

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
def admin_list_tenants(
    db: Session = Depends(get_db)
):
    tenants = list_tenants(db)

    return {
        "total": len(tenants),
        "tenants": [
            {
                "id": t.id,
                "company_name": t.company_name,
                "owner_email": t.owner_email,
                "subscription_tier": str(t.subscription_tier),
                "billing_active": t.is_billing_active
            }
            for t in tenants
        ]
    }


@router.get("/tenant/{tenant_id}")
def admin_get_tenant(
    tenant_id: str,
    db: Session = Depends(get_db)
):
    tenant = get_tenant(db, tenant_id)

    if not tenant:
        return {
            "status": "NOT_FOUND"
        }

    return tenant


@router.patch("/tenant/{tenant_id}/billing")
def admin_update_billing(
    tenant_id: str,
    active: bool,
    db: Session = Depends(get_db)
):
    tenant = update_billing_status(
        db,
        tenant_id,
        active
    )

    if not tenant:
        return {
            "status": "NOT_FOUND"
        }

    return {
        "status": "UPDATED",
        "tenant_id": tenant.id,
        "billing_active": tenant.is_billing_active
    }
