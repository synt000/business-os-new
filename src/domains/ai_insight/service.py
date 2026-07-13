from datetime import datetime, time

from sqlalchemy.orm import Session
from sqlalchemy import func

from src.models.saas_core import (
    Product,
    SupplierPayable,
    Customer,
    Order,
    Payment,
)


def generate_business_insights(
    db: Session,
    tenant_id: str
):

    insights = []


    # =========================
    # SALES PERFORMANCE
    # =========================

    today_start = datetime.combine(
        datetime.utcnow().date(),
        time.min
    )


    today_revenue = (
        db.query(
            func.coalesce(
                func.sum(Order.total_amount),
                0
            )
        )
        .filter(
            Order.tenant_id == tenant_id,
            Order.created_at >= today_start
        )
        .scalar()
    )


    today_orders = (
        db.query(Order)
        .filter(
            Order.tenant_id == tenant_id,
            Order.created_at >= today_start
        )
        .count()
    )


    insights.append({

        "title": "Sales Performance",

        "message":
        f"ဒီနေ့ Order {today_orders} ခု၊ ရောင်းအား {today_revenue} ရှိပါသည်",

        "level":
        "INFO"

    })


    # =========================
    # STOCK CHECK
    # =========================

    products = (
        db.query(Product)
        .filter(
            Product.tenant_id == tenant_id
        )
        .all()
    )


    for product in products:

        if product.stock_qty <= product.low_stock_threshold:

            insights.append({

                "title":
                "Low Stock Alert",

                "message":
                f"{product.name} လက်ကျန် {product.stock_qty} ခုသာ ကျန်ရှိပါသည်",

                "level":
                "WARNING"

            })


    # =========================
    # SUPPLIER DEBT
    # =========================

    payables = (
        db.query(SupplierPayable)
        .filter(
            SupplierPayable.tenant_id == tenant_id
        )
        .all()
    )


    total_debt = sum(
        x.balance_amount or 0
        for x in payables
    )


    if total_debt > 0:

        insights.append({

            "title":
            "Supplier Debt",

            "message":
            f"Supplier အကြွေး {total_debt} ရှိပါသည်",

            "level":
            "INFO"

        })


    # =========================
    # CUSTOMER
    # =========================

    customers = (
        db.query(Customer)
        .filter(
            Customer.tenant_id == tenant_id
        )
        .count()
    )


    insights.append({

        "title":
        "Customer Growth",

        "message":
        f"Customer စုစုပေါင်း {customers} ယောက်ရှိပါသည်",

        "level":
        "INFO"

    })


    # =========================
    # PAYMENT COLLECTION
    # =========================

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


    insights.append({

        "title":
        "Payment Collection",

        "message":
        f"လက်ခံရရှိငွေ {collected} ရှိပါသည်",

        "level":
        "INFO"

    })


    return insights
