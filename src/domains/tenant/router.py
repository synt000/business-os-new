from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database import get_db
from src.domains.tenant.service import create_tenant


router = APIRouter(
    prefix="/api/v1/tenants",
    tags=["Tenant"]
)


@router.post("/", status_code=201)
def register_tenant(
    payload: dict,
    db: Session = Depends(get_db)
):
    name = payload.get("name")

    tenant = create_tenant(
        db,
        name
    )

    return {
        "message": "Tenant created successfully",
        "tenant_id": tenant.id,
        "name": tenant.company_name,
        "plan": (
            tenant.subscription_tier.value
            if hasattr(tenant.subscription_tier, "value")
            else tenant.subscription_tier
        ),
        "trial_end": tenant.trial_expired
    }
