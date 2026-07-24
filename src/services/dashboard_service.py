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

        today = DashboardService.get_today_stats(
            db,
            tenant_id
        )

        chart = DashboardService.get_revenue_chart(
            db,
            tenant_id
        )

        return {
            # Existing API fields
            "products": products,
            "orders": orders,
            "customers": customers,
            "suppliers": suppliers,
            "revenue": revenue or 0,
            "credit_alerts": alerts,

            # Dashboard frontend compatibility
            "total_products": products,
            "total_orders": orders,
            "total_customers": customers,
            "total_suppliers": suppliers,
            "total_sales": revenue or 0,

            # Today dashboard stats
            "today_orders": today["today_orders"],
            "today_revenue": today["today_revenue"],
            "trends": today["trends"],

            # Premium Dashboard Metrics
            "new_customers": today["new_customers"],
            "low_stock": today["low_stock"],
            "social_leads": today["social_leads"],
            "notifications": today["notifications"],

            # Revenue Trend Chart
            "sales_chart": chart,
        }


    @staticmethod
    def get_revenue_chart(
        db: Session,
        tenant_id: str
    ):

        revenue_rows = (
            db.query(
                func.date(AccountLedger.created_at),
                func.sum(AccountLedger.amount)
            )
            .filter(
                AccountLedger.tenant_id == tenant_id,
                AccountLedger.entry_type == "CREDIT",
                AccountLedger.account_head == "SALES_REVENUE"
            )
            .group_by(
                func.date(AccountLedger.created_at)
            )
            .order_by(
                func.date(AccountLedger.created_at)
            )
            .all()
        )


        order_rows = (
            db.query(
                func.date(Order.created_at),
                func.count(Order.id)
            )
            .filter(
                Order.tenant_id == tenant_id
            )
            .group_by(
                func.date(Order.created_at)
            )
            .all()
        )


        order_map = {
            str(row[0]): row[1]
            for row in order_rows
        }


        return {
            "labels": [
                str(row[0])
                for row in revenue_rows
            ],

            "values": [
                float(row[1] or 0)
                for row in revenue_rows
            ],

            "revenue": [
                float(row[1] or 0)
                for row in revenue_rows
            ],

            "sales": [
                float(row[1] or 0)
                for row in revenue_rows
            ],

            "orders": [
                order_map.get(str(row[0]),0)
                for row in revenue_rows
            ]
        }


    @staticmethod
    def get_today_stats(
        db: Session,
        tenant_id: str
    ):

        from datetime import date, timedelta

        latest_sale_date = (
            db.query(func.max(func.date(AccountLedger.created_at)))
            .filter(
                AccountLedger.tenant_id == tenant_id,
                AccountLedger.entry_type == "CREDIT",
                AccountLedger.account_head == "SALES_REVENUE",
            )
            .scalar()
        )

        today = latest_sale_date or date.today()

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
                AccountLedger.account_head == "SALES_REVENUE",
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


        from datetime import datetime

        if isinstance(today, str):
            today = datetime.strptime(today, "%Y-%m-%d").date()

        previous_sale_date = (
            db.query(
                func.max(
                    func.date(AccountLedger.created_at)
                )
            )
            .filter(
                AccountLedger.tenant_id == tenant_id,
                AccountLedger.entry_type == "CREDIT",
                AccountLedger.account_head == "SALES_REVENUE",
                func.date(AccountLedger.created_at) < today
            )
            .scalar()
        )

        yesterday = previous_sale_date

        if isinstance(yesterday, str):
            yesterday = datetime.strptime(
                yesterday,
                "%Y-%m-%d"
            ).date()

        yesterday_customers = (
            db.query(Customer)
            .filter(
                Customer.tenant_id == tenant_id,
                func.date(Customer.created_at) == yesterday
            )
            .count()
        )

        if yesterday_customers > 0:
            customer_growth = (
                (new_customers - yesterday_customers)
                / yesterday_customers
                * 100
            )
        else:
            customer_growth = 0


        yesterday_orders = (
            db.query(Order)
            .filter(
                Order.tenant_id == tenant_id,
                func.date(Order.created_at) == yesterday
            )
            .count()
        )


        yesterday_revenue = (
            db.query(func.sum(AccountLedger.amount))
            .filter(
                AccountLedger.tenant_id == tenant_id,
                AccountLedger.entry_type == "CREDIT",
                AccountLedger.account_head == "SALES_REVENUE",
                func.date(AccountLedger.created_at) == yesterday
            )
            .scalar()
            or 0
        )


        if yesterday_revenue and float(yesterday_revenue) > 0:
            revenue_growth = (
                (float(today_revenue) - float(yesterday_revenue))
                / float(yesterday_revenue)
                * 100
            )
        else:
            revenue_growth = 0

        # Premium KPI display limit

        if yesterday_orders and yesterday_orders > 0:
            orders_growth = (
                (today_orders - yesterday_orders)
                / yesterday_orders
                * 100
            )
        else:
            orders_growth = 0


        if not yesterday_revenue and today_revenue > 0:
            growth_label = "NEW"
        elif revenue_growth > 0:
            growth_label = f"↑ {round(revenue_growth,1)}%"
        elif revenue_growth < 0:
            growth_label = f"↓ {abs(round(revenue_growth,1))}%"
        else:
            growth_label = "0%"

        print("DEBUG TODAY:", {
            "today_revenue": today_revenue,
            "yesterday_revenue": yesterday_revenue,
            "revenue_growth": revenue_growth,
            "growth_label": growth_label,
        }, flush=True)

        trends = {
            "revenue_growth": round(revenue_growth,1),
            "orders_growth": round(orders_growth,1),
            "customer_growth": round(customer_growth,1),
            "growth_label": growth_label
        }


        return {
            "today_orders": today_orders,
            "today_revenue": float(today_revenue),
            "new_customers": new_customers,
            "low_stock": low_stock,
            "social_leads": social_leads,
            "notifications": notifications,
            "trends": trends
        }

