from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import Session

from src.models.saas_core import Order, Payment


def get_revenue_summary(
    db: Session,
    tenant_id: str,
    start_at: datetime,
    end_at: datetime,
):
    row = (
        db.query(
            func.coalesce(func.sum(Payment.amount), 0.0),
            func.count(Payment.id),
        )
        .filter(
            Payment.tenant_id == tenant_id,
            Payment.status == "COMPLETED",
            Payment.created_at >= start_at,
            Payment.created_at < end_at,
        )
        .one()
    )

    return {
        "revenue": float(row[0] or 0.0),
        "payment_count": int(row[1] or 0),
    }


def get_daily_revenue(
    db: Session,
    tenant_id: str,
    start_at: datetime,
    end_at: datetime,
):
    payments = (
        db.query(Payment.created_at, Payment.amount)
        .filter(
            Payment.tenant_id == tenant_id,
            Payment.status == "COMPLETED",
            Payment.created_at >= start_at,
            Payment.created_at < end_at,
        )
        .order_by(Payment.created_at.asc())
        .all()
    )

    totals = {}

    for created_at, amount in payments:
        day = created_at.date().isoformat()
        totals[day] = totals.get(day, 0.0) + float(amount or 0.0)

    return [
        {
            "date": day,
            "revenue": totals[day],
        }
        for day in sorted(totals)
    ]


def get_order_summary(
    db: Session,
    tenant_id: str,
    start_at: datetime,
    end_at: datetime,
):
    row = (
        db.query(
            func.count(Order.id),
            func.coalesce(func.sum(Order.total_amount), 0.0),
        )
        .filter(
            Order.tenant_id == tenant_id,
            Order.order_status == "PAID",
            Order.created_at >= start_at,
            Order.created_at < end_at,
        )
        .one()
    )

    order_count = int(row[0] or 0)
    order_value = float(row[1] or 0.0)

    return {
        "order_count": order_count,
        "order_value": order_value,
        "average_order_value": (
            order_value / order_count
            if order_count
            else 0.0
        ),
    }


def get_daily_order_summary(
    db: Session,
    tenant_id: str,
    start_at: datetime,
    end_at: datetime,
):
    orders = (
        db.query(Order.created_at, Order.total_amount)
        .filter(
            Order.tenant_id == tenant_id,
            Order.order_status == "PAID",
            Order.created_at >= start_at,
            Order.created_at < end_at,
        )
        .order_by(Order.created_at.asc())
        .all()
    )

    totals = {}

    for created_at, amount in orders:
        day = created_at.date().isoformat()

        if day not in totals:
            totals[day] = {
                "order_count": 0,
                "order_value": 0.0,
            }

        totals[day]["order_count"] += 1
        totals[day]["order_value"] += float(amount or 0.0)

    return [
        {
            "date": day,
            "order_count": totals[day]["order_count"],
            "order_value": totals[day]["order_value"],
            "average_order_value": (
                totals[day]["order_value"] / totals[day]["order_count"]
                if totals[day]["order_count"]
                else 0.0
            ),
        }
        for day in sorted(totals)
    ]


def get_customer_count(
    db: Session,
    tenant_id: str,
    start_at: datetime,
    end_at: datetime,
) -> int:
    return int(
        db.query(func.count(func.distinct(Order.customer_name)))
        .filter(
            Order.tenant_id == tenant_id,
            Order.order_status == "PAID",
            Order.created_at >= start_at,
            Order.created_at < end_at,
            Order.customer_name.isnot(None),
        )
        .scalar()
        or 0
    )
