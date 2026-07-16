from sqlalchemy.orm import Session
from sqlalchemy import func

from src.models.saas_core import (
    Order,
    Customer,
    Supplier,
    AccountLedger,
    CustomerCreditAlert,
)

from src.domains.product.models import Product


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

        revenue = (
            db.query(func.sum(AccountLedger.amount))
            .filter(
                AccountLedger.tenant_id == tenant_id,
                AccountLedger.entry_type == "CREDIT",
                AccountLedger.account_head.in_([
                    "SALES_REVENUE",
                    "SUBSCRIPTION_REVENUE"
                ])
            )
            .scalar()
            or 0
        )

        alerts = (
            db.query(CustomerCreditAlert)
            .filter(CustomerCreditAlert.tenant_id == tenant_id)
            .count()
        )

        return {
            "products": products,
            "orders": orders,
            "customers": customers,
            "suppliers": suppliers,
            "revenue": revenue,
            "credit_alerts": alerts,
        }
