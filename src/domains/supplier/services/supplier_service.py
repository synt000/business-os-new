from sqlalchemy.orm import Session

from src.models.saas_core import Supplier
from src.domains.supplier.schemas import SupplierCreate


def create_supplier(
    db: Session,
    tenant_id: str,
    data: SupplierCreate,
):
    supplier = Supplier(
        tenant_id=tenant_id,
        supplier_name=data.supplier_name,
        contact_phone=data.contact_phone,
    )

    db.add(supplier)
    db.commit()
    db.refresh(supplier)

    return supplier


def get_suppliers(
    db: Session,
    tenant_id: str,
):
    return (
        db.query(Supplier)
        .filter(Supplier.tenant_id == tenant_id)
        .order_by(Supplier.created_at.desc())
        .all()
    )
