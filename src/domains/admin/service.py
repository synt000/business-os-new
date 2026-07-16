from sqlalchemy.orm import Session

from src.models.saas_core import Tenant


def list_tenants(db: Session):
    return db.query(Tenant).all()


def get_tenant(db: Session, tenant_id: str):
    return (
        db.query(Tenant)
        .filter(Tenant.id == tenant_id)
        .first()
    )


def update_billing_status(
    db: Session,
    tenant_id: str,
    active: bool
):
    tenant = get_tenant(db, tenant_id)

    if not tenant:
        return None

    tenant.is_billing_active = active
    db.commit()
    db.refresh(tenant)

    return tenant
