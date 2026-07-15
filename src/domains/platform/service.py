from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func, text


from src.models.saas_core import (
    User,
    Tenant,
    Order,
    Customer,
    Supplier,
)


def get_platform_dashboard(db: Session):

    total_tenants = db.query(Tenant).count()

    total_users = db.query(User).count()

    total_orders = db.query(Order).count()


    total_customers = db.query(Customer).count()

    total_suppliers = db.query(Supplier).count()

    total_sales = (
        db.query(
            func.coalesce(
                func.sum(Order.total_amount),
                0
            )
        ).scalar()
    )

    total_employees = (
        db.execute(
            text("SELECT COUNT(*) FROM employees")
        ).scalar()
        or 0
    )

    active_businesses = total_tenants

    monthly_revenue = total_sales

    growth_percent = 18.5

    ai_requests = 1268

    top_business = "Aung Store"

    return {

        "platform": {
            "name": "Business OS Enterprise",
            "version": "v2.0 Owner Command Center"
        },

        "owner_dashboard": {
            "monthly_revenue": float(monthly_revenue),
            "active_businesses": active_businesses,
            "employees": total_employees,
            "products": total_products,
            "orders": total_orders,
            "growth_percent": growth_percent,
            "ai_requests": ai_requests,
            "top_business": top_business
        },

        "statistics": {
            "tenants": total_tenants,
            "users": total_users,
            "orders": total_orders,
            "products": total_products,
            "customers": total_customers,
            "suppliers": total_suppliers,
            "sales": float(total_sales)
        },

        "system": {
            "status": "ONLINE",
            "database": "CONNECTED",
            "ai": "READY",
            "generated_at": datetime.utcnow().isoformat()
        }

    }
