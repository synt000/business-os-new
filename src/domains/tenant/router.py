from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database import get_db
from src.domains.tenant.service import create_tenant

router = APIRouter(
    prefix="/tenant",
    tags=["Tenant"]
)


@router.post("/register")
def register_tenant(
    name: str,
    db: Session = Depends(get_db)
):

    tenant = create_tenant(db, name)

    return {
        "message": "Tenant created successfully",
        "tenant_id": tenant.id,
        "name": tenant.name,
        "plan": tenant.plan,
        "trial_end": tenant.trial_end
    }
