from sqlalchemy.orm import Session

from src.models.saas_core import Customer


def create_customer(
    db: Session,
    tenant_id: str,
    data,
):
    customer = Customer(
        tenant_id=tenant_id,
        customer_name=data.full_name,
        customer_phone=data.phone,
        customer_email=data.email,
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
