from sqlalchemy.orm import Session
from sqlalchemy import func

from src.models.saas_core import (
    Order,
    Customer,
    Supplier,
    CustomerCreditAlert,
)

from src.domains.accounting.models import AccountLedger

from src.domains.product.models import Product
from src.domains.inventory.models import Inventory


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


    @staticmethod
    def get_revenue_chart(
        db: Session,
        tenant_id: str
    ):

        rows = (
            db.query(
                func.date(AccountLedger.created_at),
                func.sum(AccountLedger.amount)
            )
            .filter(
                AccountLedger.tenant_id == tenant_id,
                AccountLedger.entry_type == "CREDIT"
            )
            .group_by(
                func.date(AccountLedger.created_at)
            )
            .order_by(
                func.date(AccountLedger.created_at)
            )
            .all()
        )

        return {
            "labels": [
                str(row[0])
                for row in rows
            ],
            "values": [
                float(row[1] or 0)
                for row in rows
            ],
            "revenue": [
                float(row[1] or 0)
                for row in rows
            ],
            "sales": [
                float(row[1] or 0)
                for row in rows
            ],
            "orders": []
        }


    @staticmethod
    def get_today_stats(
        db: Session,
        tenant_id: str
    ):

        from datetime import date

        today = date.today()

        today_orders = (
            db.query(Order)
            .filter(
                Order.tenant_id == tenant_id,
                func.date(Order.created_at) == today
            )
            .count()
        )


        today_revenue = (
            db.query(func.sum(AccountLedger.amount))
            .filter(
                AccountLedger.tenant_id == tenant_id,
                AccountLedger.entry_type == "CREDIT",
                func.date(AccountLedger.created_at) == today
            )
            .scalar()
            or 0
        )


        new_customers = (
            db.query(Customer)
            .filter(
                Customer.tenant_id == tenant_id,
                func.date(Customer.created_at) == today
            )
            .count()
        )


        low_stock = (
            db.query(Inventory)
            .filter(
                Inventory.tenant_id == tenant_id,
                Inventory.quantity <= Inventory.low_stock_threshold
            )
            .count()
        )


        try:
            from src.domains.social_center.models import SocialLead

            social_leads = (
                db.query(SocialLead)
                .filter(
                    SocialLead.tenant_id == tenant_id
                )
                .count()
            )

        except Exception:
            social_leads = 0


        notifications = 0


        return {
            "today_orders": today_orders,
            "today_revenue": float(today_revenue),
            "new_customers": new_customers,
            "low_stock": low_stock,
            "social_leads": social_leads,
            "notifications": notifications
        }

