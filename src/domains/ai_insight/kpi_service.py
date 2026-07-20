from datetime import datetime, date

from sqlalchemy.orm import Session
from sqlalchemy import func

from src.models.saas_core import Order, Payment


class KPIService:

    @staticmethod
    def get_sales_kpi(
        db: Session,
        tenant_id: str
    ):

        total_sales = (
            db.query(
                func.coalesce(
                    func.sum(Order.total_amount),
                    0
                )
            )
            .filter(
                Order.tenant_id == tenant_id
            )
            .scalar()
        )

        orders = (
            db.query(func.count(Order.id))
            .filter(
                Order.tenant_id == tenant_id
            )
            .scalar()
        )

        today_sales = (
            db.query(
                func.coalesce(
                    func.sum(Order.total_amount),
                    0
                )
            )
            .filter(
                Order.tenant_id == tenant_id,
                func.date(Order.created_at) == str(date.today())
            )
            .scalar()
        )

        return {
            "total_sales": float(total_sales or 0),
            "orders": orders or 0,
            "today_sales": float(today_sales or 0),
            "average_order": (
                float(total_sales or 0) / orders
                if orders
                else 0
            )
        }


    @staticmethod
    def get_finance_kpi(
        db: Session,
        tenant_id: str
    ):

        collected = (
            db.query(
                func.coalesce(
                    func.sum(Payment.amount),
                    0
                )
            )
            .filter(
                Payment.tenant_id == tenant_id,
                Payment.status == "COMPLETED"
            )
            .scalar()
        )

        payments = (
            db.query(func.count(Payment.id))
            .filter(
                Payment.tenant_id == tenant_id
            )
            .scalar()
        )

        return {
            "collected_cash": float(collected or 0),
            "payment_count": payments or 0
        }


    @staticmethod
    def get_ceo_summary(
        db: Session,
        tenant_id: str
    ):

        sales = KPIService.get_sales_kpi(
            db,
            tenant_id
        )

        finance = KPIService.get_finance_kpi(
            db,
            tenant_id
        )

        return {
            "sales": sales,
            "finance": finance,
            "health_score": 50
        }
