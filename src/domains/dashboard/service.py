from datetime import datetime, time

from sqlalchemy.orm import Session
from sqlalchemy import func

from src.domains.product.models import Product
from src.domains.inventory.models import Inventory


from src.models.saas_core import (
    TenantFeature,
    DashboardMenu,
    Order,
    Customer,
    Payment,
    Supplier,
    SupplierPayable,
    Invoice,
    AccountLedger,
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
        .join(Inventory)
        .filter(
            Product.tenant_id == tenant_id,
            Inventory.quantity <= Product.reorder_level
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

    low_stock = (
        db.query(Product)
        .join(Inventory)
        .filter(
            Product.tenant_id == tenant_id,
            Inventory.quantity <= Product.reorder_level
        )
        .count()
    )


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


def get_financial_kpi_summary(
    db: Session,
    tenant_id: str
):

    cash_balance = (
        db.query(
            func.coalesce(
                func.sum(AccountLedger.amount),
                0
            )
        )
        .filter(
            AccountLedger.tenant_id == tenant_id,
            AccountLedger.account_head == "CASH_ASSET"
        )
        .scalar()
    )


    supplier_payable = (
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


    customer_receivable = (
        db.query(
            func.coalesce(
                func.sum(Invoice.amount),
                0
            )
        )
        .filter(
            Invoice.tenant_id == tenant_id,
            Invoice.status != "PAID"
        )
        .scalar()
    )


    revenue = (
        db.query(
            func.coalesce(
                func.sum(Invoice.amount),
                0
            )
        )
        .filter(
            Invoice.tenant_id == tenant_id
        )
        .scalar()
    )


    purchase_cost = (
        db.query(
            func.coalesce(
                func.sum(AccountLedger.amount),
                0
            )
        )
        .filter(
            AccountLedger.tenant_id == tenant_id,
            AccountLedger.account_head == "INVENTORY_ASSET"
        )
        .scalar()
    )


    estimated_profit = (
        revenue - purchase_cost
    )


    health = 50


    if estimated_profit > 0:
        health += 30


    if supplier_payable < revenue:
        health += 20


    if health > 100:
        health = 100


    return {
        "cash_balance": cash_balance,
        "supplier_payable": supplier_payable,
        "customer_receivable": customer_receivable,
        "revenue": revenue,
        "purchase_cost": purchase_cost,
        "estimated_profit": estimated_profit,
        "finance_health": health
    }


def get_finance_insight(
    db: Session,
    tenant_id: str
):
    """
    AI Finance Insight Engine
    """

    from sqlalchemy import func

    # Revenue
    revenue = (
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


    # Supplier Payable
    supplier_payable = (
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


    # Invoice Receivable
    customer_receivable = (
        db.query(
            func.coalesce(
                func.sum(Invoice.amount),
                0
            )
        )
        .filter(
            Invoice.tenant_id == tenant_id
        )
        .scalar()
    )


    # Cash Ledger
    cash_balance = (
        db.query(
            func.coalesce(
                func.sum(AccountLedger.amount),
                0
            )
        )
        .filter(
            AccountLedger.tenant_id == tenant_id,
            AccountLedger.account_head == "CASH_ASSET"
        )
        .scalar()
    )


    purchase_cost = (
        db.query(
            func.coalesce(
                func.sum(AccountLedger.amount),
                0
            )
        )
        .filter(
            AccountLedger.tenant_id == tenant_id,
            AccountLedger.account_head == "INVENTORY_ASSET"
        )
        .scalar()
    )


    profit = revenue - purchase_cost


    health = 50

    if profit > 0:
        health += 30

    if cash_balance > supplier_payable:
        health += 20


    if health > 100:
        health = 100


    return {
        "cash_balance": float(cash_balance),
        "supplier_payable": float(supplier_payable),
        "customer_receivable": float(customer_receivable),
        "revenue": float(revenue),
        "purchase_cost": float(purchase_cost),
        "estimated_profit": float(profit),
        "finance_health": health
    }


def get_owner_platform_summary(
    db: Session
):
    """
    Platform Owner Command Center Summary
    """

    from src.models.saas_core import (
        Tenant,
        User
    )

    total_businesses = (
        db.query(Tenant)
        .count()
    )

    total_users = (
        db.query(User)
        .count()
    )


    total_orders = 0
    total_sales = 0


    try:
        total_orders = (
            db.query(Order)
            .count()
        )

        total_sales = (
            db.query(
                func.coalesce(
                    func.sum(Order.total_amount),
                    0
                )
            )
            .scalar()
        )

    except Exception:
        pass


    return {

        "businesses": total_businesses,

        "users": total_users,

        "orders": total_orders,

        "sales": float(total_sales or 0),

        "system_health": "100%"

    }


def get_owner_platform_summary(
    db,
    tenant_id=None
):
    from src.models.saas_core import User, Tenant
    from src.domains.order.models import Order
    from sqlalchemy import func

    tenants = db.query(func.count(Tenant.id)).scalar() or 0

    users = db.query(func.count(User.id)).scalar() or 0

    orders = db.query(func.count(Order.id)).scalar() or 0

    sales = (
        db.query(func.coalesce(func.sum(Order.total_amount),0))
        .scalar()
        or 0
    )

    return {
        "tenants": tenants,
        "users": users,
        "orders": orders,
        "sales": float(sales)
    }



def get_owner_platform_summary(db: Session):
    """
    Owner SaaS Platform Summary V2
    """

    from src.models.saas_core import User, Tenant
    from src.domains.order.models import Order
    from sqlalchemy import func


    total_users = (
        db.query(func.count(User.id))
        .scalar()
        or 0
    )


    total_businesses = (
        db.query(func.count(Tenant.id))
        .scalar()
        or 0
    )


    total_orders = 0
    total_sales = 0


    try:

        total_orders = (
            db.query(func.count(Order.id))
            .scalar()
            or 0
        )


        total_sales = (
            db.query(
                func.coalesce(
                    func.sum(Order.total_amount),
                    0
                )
            )
            .scalar()
            or 0
        )


    except Exception as e:
        print(
            "OWNER SUMMARY ERROR:",
            e
        )


    return {

        "total_users": total_users,

        "total_businesses": total_businesses,

        "total_orders": total_orders,

        "total_sales": float(total_sales),

        "monthly_growth": 0,

        "system_status": "ONLINE"

    }
