from sqlalchemy import func
from src.models.saas_core import Customer

def customer_widget(db, tenant_id):
    total_customers = (
        db.query(func.count(Customer.id))
        .filter(Customer.tenant_id == tenant_id)
        .scalar()
    ) or 0

    return {
        "total_customers": total_customers,
        "new_customers": 0,
        "returning_customers": 0,
        "active_customers": total_customers,
    }
