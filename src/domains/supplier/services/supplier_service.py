import uuid

from sqlalchemy.orm import Session

from src.models.saas_core import Supplier


def create_supplier(
    db: Session,
    tenant_id: str,
    data,
):
    supplier = Supplier(
        id=str(uuid.uuid4()),
        supplier_name=data.supplier_name,
        contact_phone=data.contact_phone,
        tenant_id=tenant_id,
    )

    db.add(supplier)
    db.commit()
    db.refresh(supplier)

    return supplier


def list_suppliers(
    db: Session,
    tenant_id: str,
):
    return (
        db.query(Supplier)
        .filter(Supplier.tenant_id == tenant_id)
        .order_by(Supplier.created_at.desc())
        .all()
    )
