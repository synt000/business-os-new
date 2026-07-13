from datetime import datetime, time

from sqlalchemy.orm import Session
from sqlalchemy import func

from src.models.saas_core import (
    TenantFeature,
    DashboardMenu,
    Product,
    Order,
    Customer,
    Payment,
    Supplier,
    SupplierPayable,
)


def get_dashboard_menus(
    db: Session,
    tenant_id: str
):
    features = (
        db.query(TenantFeature.feature_code)
        .filter(
            TenantFeature.tenant_id == tenant_id,
            TenantFeature.enabled == True
        )
        .all()
    )

    feature_codes = [
        x[0]
        for x in features
    ]

    return (
        db.query(DashboardMenu)
        .filter(
            DashboardMenu.feature_code.in_(feature_codes)
        )
        .all()
    )


def get_ceo_dashboard_summary(
    db: Session,
    tenant_id: str
):

    today_start = datetime.combine(
        datetime.utcnow().date(),
        time.min
    )


    # TODAY SALES

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


    # TOTAL ORDERS

    total_orders = (
        db.query(Order)
        .filter(
            Order.tenant_id == tenant_id
        )
        .count()
    )


    # TOTAL SALES

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


    total_products = (
        db.query(Product)
        .filter(
            Product.tenant_id == tenant_id
        )
        .count()
    )


    total_customers = (
        db.query(Customer)
        .filter(
            Customer.tenant_id == tenant_id
        )
        .count()
    )


    total_suppliers = (
        db.query(Supplier)
        .filter(
            Supplier.tenant_id == tenant_id
        )
        .count()
    )


    low_stock = (
        db.query(Product)
        .filter(
            Product.tenant_id == tenant_id,
            Product.stock_qty <= Product.low_stock_threshold
        )
        .count()
    )


    completed_payments = (
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


    return {

        "today_revenue": today_revenue,
        "today_orders": today_orders,

        "total_orders": total_orders,
        "total_sales": total_sales,

        "total_products": total_products,
        "total_customers": total_customers,
        "total_suppliers": total_suppliers,

        "low_stock": low_stock,

        "completed_payments": completed_payments

    }


def get_business_health_score(
    db: Session,
    tenant_id: str
):
    """
    AI Business Health Engine
    """

    score = 0
    details = {}


    # Sales Score (30)
    total_sales = (
        db.query(func.coalesce(func.sum(Order.total_amount), 0))
        .filter(
            Order.tenant_id == tenant_id
        )
        .scalar()
    )

    if total_sales > 0:
        sales_score = 30
    else:
        sales_score = 10

    score += sales_score
    details["sales"] = sales_score



    # Product Stock Score (25)
    low_stock = (
        db.query(Product)
        .filter(
            Product.tenant_id == tenant_id,
            Product.stock_qty <= Product.low_stock_threshold
        )
        .count()
    )

    if low_stock == 0:
        stock_score = 25
    elif low_stock <= 2:
        stock_score = 20
    else:
        stock_score = 10

    score += stock_score
    details["inventory"] = stock_score



    # Customer Score (20)
    customers = (
        db.query(Customer)
        .filter(
            Customer.tenant_id == tenant_id
        )
        .count()
    )

    if customers >= 10:
        customer_score = 20
    elif customers > 0:
        customer_score = 15
    else:
        customer_score = 5

    score += customer_score
    details["customer"] = customer_score



    # Payment Score (25)
    payments = (
        db.query(
            func.coalesce(func.sum(Payment.amount),0)
        )
        .filter(
            Payment.tenant_id == tenant_id,
            Payment.status == "COMPLETED"
        )
        .scalar()
    )


    if payments > 0:
        payment_score = 25
    else:
        payment_score = 10


    score += payment_score
    details["payment"] = payment_score



    if score >= 90:
        level = "A+ EXCELLENT"
    elif score >= 75:
        level = "GOOD"
    elif score >= 50:
        level = "WARNING"
    else:
        level = "CRITICAL"



    return {
        "health_score": score,
        "level": level,
        "details": details
    }


from datetime import timedelta


def get_sales_trend(
    db: Session,
    tenant_id: str
):
    """
    Last 7 Days Sales Trend
    """

    result = []

    today = datetime.utcnow().date()

    for i in range(6, -1, -1):

        day = today - timedelta(days=i)

        start = datetime.combine(day, time.min)
        end = datetime.combine(day, time.max)

        revenue = (
            db.query(
                func.coalesce(
                    func.sum(Order.total_amount),
                    0
                )
            )
            .filter(
                Order.tenant_id == tenant_id,
                Order.created_at >= start,
                Order.created_at <= end
            )
            .scalar()
        )

        orders = (
            db.query(Order)
            .filter(
                Order.tenant_id == tenant_id,
                Order.created_at >= start,
                Order.created_at <= end
            )
            .count()
        )

        result.append({
            "date": str(day),
            "sales": float(revenue),
            "orders": orders
        })

    return result



def get_revenue_expense_summary(
    db: Session,
    tenant_id: str
):
    revenue = (
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

    expense = (
        db.query(
            func.coalesce(
                func.sum(SupplierPayable.balance_amount),
                0
            )
        )
        .filter(
            SupplierPayable.tenant_id == tenant_id
        )
        .scalar()
    )

    return {
        "revenue": float(revenue),
        "expense": float(expense),
        "profit": float(revenue - expense)
    }
