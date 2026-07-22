from datetime import datetime, timedelta

from src.models.saas_core import Order


def sales_widget(db, tenant_id):

    now = datetime.utcnow()

    today_start = datetime(
        now.year,
        now.month,
        now.day
    )

    month_start = datetime(
        now.year,
        now.month,
        1
    )

    today_orders = (
        db.query(Order)
        .filter(
            Order.tenant_id == tenant_id,
            Order.created_at >= today_start
        )
        .count()
    )

    today_revenue = (
        db.query(Order)
        .filter(
            Order.tenant_id == tenant_id,
            Order.created_at >= today_start
        )
        .with_entities(Order.total_amount)
        .all()
    )

    today_revenue = sum(
        x[0] or 0
        for x in today_revenue
    )


    monthly_revenue = (
        db.query(Order)
        .filter(
            Order.tenant_id == tenant_id,
            Order.created_at >= month_start
        )
        .with_entities(Order.total_amount)
        .all()
    )

    monthly_revenue = sum(
        x[0] or 0
        for x in monthly_revenue
    )


    return {
        "title": "Sales",
        "today_orders": today_orders,
        "today_revenue": today_revenue,
        "monthly_revenue": monthly_revenue,
        "currency": "MMK"
    }
