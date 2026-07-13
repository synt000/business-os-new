from sqlalchemy.orm import Session
from sqlalchemy import func

from src.models.saas_core import (
    Product,
    Order,
    Customer,
    Supplier,
    AccountLedger,
    CustomerCreditAlert,
)


class DashboardService:

    @staticmethod
    def get_summary(
        db: Session,
        tenant_id: str
    ):

        products = (
            db.query(Product)
            .filter(Product.tenant_id == tenant_id)
            .count()
        )

        orders = (
            db.query(Order)
            .filter(Order.tenant_id == tenant_id)
            .count()
        )

        customers = (
            db.query(Customer)
            .filter(Customer.tenant_id == tenant_id)
            .count()
        )

        suppliers = (
            db.query(Supplier)
            .filter(Supplier.tenant_id == tenant_id)
            .count()
        )

        sales_total = (
            db.query(func.sum(AccountLedger.amount))
            .filter(
                AccountLedger.tenant_id == tenant_id,
                AccountLedger.account_head == "SALES_REVENUE"
            )
            .scalar()
            or 0
        )

        credit_alerts = (
            db.query(CustomerCreditAlert)
            .filter(
                CustomerCreditAlert.tenant_id == tenant_id,
                CustomerCreditAlert.status == "OPEN"
            )
            .count()
        )

        return {
            "products": products,
            "orders": orders,
            "customers": customers,
            "suppliers": suppliers,
            "sales_total": round(sales_total, 2),
            "credit_alerts": credit_alerts
        }
