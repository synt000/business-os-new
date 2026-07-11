from sqlalchemy.orm import Session

from src.models.saas_core import Customer


def create_customer(
    db: Session,
    tenant_id: str,
    data,
):
    customer = Customer(
        tenant_id=tenant_id,
        full_name=data.full_name,
        phone=data.phone,
        email=data.email,
        address=data.address,
    )

    db.add(customer)
    db.commit()
    db.refresh(customer)

    return customer


def get_customers(
    db: Session,
    tenant_id: str,
):
    return (
        db.query(Customer)
        .filter(Customer.tenant_id == tenant_id)
        .order_by(Customer.created_at.desc())
        .all()
    )
