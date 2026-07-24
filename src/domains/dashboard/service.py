from datetime import datetime, time

from sqlalchemy.orm import Session
from sqlalchemy import func

from src.models.saas_core import (
    User,
    Tenant,
    Customer,
    Supplier,
    Payment,
    Invoice,
)

from src.domains.order.models import Order, OrderItem


from src.domains.purchase.models import (
    SupplierPayable,
)

from src.domains.product.models import Product
from src.domains.inventory.models import Inventory
from src.domains.accounting.models import AccountLedger










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
    Synced with Dashboard Summary
    """

    from src.services.dashboard_service import DashboardService

    summary = DashboardService.get_summary(
        db,
        tenant_id
    )

    revenue = float(summary.get("revenue", 0) or 0)
    expense = float(summary.get("expense", 0) or 0)
    profit = float(summary.get("profit", 0) or 0)

    if revenue > 0:
        health = round((profit / revenue) * 100)
    else:
        health = 0

    if health > 100:
        health = 100

    return {
        "cash_balance": float(
            summary.get("total_payment",0) or 0
        ),
        "supplier_payable": 0,
        "customer_receivable": float(
            summary.get("receivable_balance",0) or 0
        ),
        "revenue": revenue,
        "purchase_cost": expense,
        "estimated_profit": profit,
        "finance_health": health,

        # AI FINANCE V2
        "margin": round(
            (profit / revenue * 100)
            if revenue > 0 else 0,
            2
        ),

        "status":
            "Healthy"
            if profit > 0
            else "Warning",

        "risk":
            "No expense data detected"
            if expense == 0
            else "Expense monitoring required",

        "ai_action":
            "Increase marketing to grow sales."
            if profit > 0
            else "Reduce expenses immediately."
    }


def get_owner_platform_summary(
    db: Session
):
    """
    Platform Owner Command Center Summary
    """







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


# ======================================
# SAAS REVENUE ANALYTICS ENGINE
# ======================================

def get_saas_revenue_summary(db):

    total_revenue = (
        db.query(
            func.coalesce(
                func.sum(SubscriptionPayment.amount),
                0
            )
        )
        .filter(
            SubscriptionPayment.status == "PAID"
        )
        .scalar()
    )


    active_subscriptions = (
        db.query(Subscription)
        .filter(
            Subscription.status == "ACTIVE"
        )
        .count()
    )


    trial_users = (
        db.query(Subscription)
        .filter(
            Subscription.is_trial == True,
            Subscription.status == "ACTIVE"
        )
        .count()
    )


    expired_users = (
        db.query(Subscription)
        .filter(
            Subscription.status == "EXPIRED"
        )
        .count()
    )


    return {
        "total_revenue": total_revenue,
        "active_subscriptions": active_subscriptions,
        "trial_users": trial_users,
        "expired_users": expired_users
    }


def get_saas_revenue_summary(
    db: Session
):
    """
    SaaS Monetization Analytics Engine
    """

    from src.domains.subscription.models import (
        Subscription,
        SubscriptionPayment,
        SubscriptionPlan
    )


    active_subscribers = (
        db.query(Subscription)
        .filter(
            Subscription.status == "ACTIVE"
        )
        .count()
    )


    monthly_revenue = (
        db.query(
            func.coalesce(
                func.sum(SubscriptionPayment.amount),
                0
            )
        )
        .filter(
            SubscriptionPayment.status == "PAID"
        )
        .scalar()
    )


    pending_payments = (
        db.query(
            SubscriptionPayment
        )
        .filter(
            SubscriptionPayment.status == "PENDING"
        )
        .count()
    )


    plans = (
        db.query(
            SubscriptionPlan
        )
        .all()
    )


    plan_summary = []

    for plan in plans:

        subscribers = (
            db.query(Subscription)
            .filter(
                Subscription.plan_id == plan.id,
                Subscription.status == "ACTIVE"
            )
            .count()
        )


        plan_summary.append(
            {
                "plan": plan.name,
                "price": plan.price,
                "subscribers": subscribers
            }
        )


    return {

        "active_subscribers":
            active_subscribers,

        "mrr":
            float(monthly_revenue or 0),

        "arr":
            float(monthly_revenue or 0) * 12,

        "pending_payments":
            pending_payments,

        "plans":
            plan_summary
    }



# ======================================
# OWNER RENEWAL CONTROL CENTER
# ======================================

def get_owner_renewal_summary(db: Session):

    from src.domains.subscription.models import Subscription
    from datetime import datetime, timedelta



    now = datetime.utcnow()

    expiring_7_days = (
        db.query(Subscription)
        .filter(
            Subscription.status == "ACTIVE",
            Subscription.end_date <= now + timedelta(days=7),
            Subscription.end_date >= now
        )
        .count()
    )


    expiring_30_days = (
        db.query(Subscription)
        .filter(
            Subscription.status == "ACTIVE",
            Subscription.end_date <= now + timedelta(days=30),
            Subscription.end_date >= now
        )
        .count()
    )


    expired = (
        db.query(Subscription)
        .filter(
            Subscription.status == "EXPIRED"
        )
        .count()
    )


    active = (
        db.query(Subscription)
        .filter(
            Subscription.status == "ACTIVE"
        )
        .count()
    )


    renewal_rate = 0

    total = active + expired

    if total:
        renewal_rate = round(
            (active / total) * 100,
            2
        )


    return {

        "expiring_7_days": expiring_7_days,

        "expiring_30_days": expiring_30_days,

        "expired": expired,

        "active_subscriptions": active,

        "renewal_rate": renewal_rate

    }



# ======================================
# AI DECISION ENGINE v8
# ======================================


def get_ai_decision_engine(
    db: Session,
    tenant_id: str
):

    finance = get_finance_insight(
        db,
        tenant_id
    )

    revenue = finance.get("revenue", 0)
    profit = finance.get("estimated_profit", 0)
    expense = finance.get("purchase_cost", 0)

    orders = (
        db.query(Order)
        .filter(Order.tenant_id == tenant_id)
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

    score = 50
    reasons = []
    actions = []

    if revenue > 0:
        score += 15
        reasons.append("✅ Revenue activity detected")
    else:
        reasons.append("⚠️ No revenue activity")

    if profit > 0:
        score += 15
        reasons.append("✅ Business is profitable")
    else:
        reasons.append("⚠️ Profit needs improvement")

    if low_stock == 0:
        score += 10
        reasons.append("✅ Inventory healthy")
    else:
        actions.append("📦 Restock fast moving products")

    if orders > 0:
        actions.append("👥 Improve customer retention")

    if revenue > expense:
        actions.append("🚀 Increase marketing budget")

    if score >= 80:
        status = "EXPANSION READY"
        decision = "🚀 Scale business and increase customer acquisition."
    elif score >= 60:
        status = "GROWING"
        decision = "📈 Continue growth strategy and optimize operations."
    else:
        status = "NEEDS ATTENTION"
        decision = "⚠️ Review sales, cost and inventory."

    return {
        "business_score": score,
        "status": status,
        "reasons": reasons,
        "recommended_actions": actions,
        "ceo_decision": decision
    }


# ======================================
# AI GROWTH PLAN ENGINE v1
# ======================================

def get_ai_growth_plan(
    db: Session,
    tenant_id: str
):

    total_sales = (
        db.query(func.coalesce(func.sum(Order.total_amount), 0))
        .filter(
            Order.tenant_id == tenant_id
        )
        .scalar()
    )

    total_orders = (
        db.query(Order)
        .filter(
            Order.tenant_id == tenant_id
        )
        .count()
    )

    if total_sales > 0:

        status = "GROWTH"

        summary = (
            f"Business generated {total_sales:.0f} MMK "
            f"from {total_orders} orders. "
            "Focus on expansion."
        )

    else:

        status = "START"

        summary = (
            "No sales activity detected. "
            "Focus on customer acquisition."
        )


    return {

        "status": status,

        "summary": summary,

        "weekly_plan":[

            {
                "week":"Week 1",
                "action":"🚀 Promote best selling products"
            },

            {
                "week":"Week 2",
                "action":"👥 Improve customer retention"
            },

            {
                "week":"Week 3",
                "action":"📦 Optimize inventory level"
            },

            {
                "week":"Week 4",
                "action":"📊 Review profit and scale strategy"
            }

        ]

    }


# ======================================
# SMART RESTOCK AI ENGINE v1
# ======================================

def get_smart_restock(
    db: Session,
    tenant_id: str
):

    low_stock_items = (
        db.query(Inventory)
        .join(Product)
        .filter(
            Inventory.tenant_id == tenant_id,
            Inventory.quantity <= Inventory.low_stock_threshold
        )
        .all()
    )


    recommendations = []


    for item in low_stock_items:

        recommendations.append({

            "product":
            item.product.name,

            "current_stock":
            item.quantity,

            "threshold":
            item.low_stock_threshold,

            "recommended_purchase":
            "Increase stock",

            "reason":
            "Stock below safety level"

        })


    if recommendations:

        health = "⚠️ Low stock items detected."

        message = (
            "Monitor low stock products "
            "and replenish inventory."
        )

    else:

        health = "✅ Stock level appears stable."

        message = (
            "Inventory is healthy. "
            "No urgent restock needed."
        )


    return {

        "status":
        "ANALYZED",

        "inventory_health":
        health,

        "recommendations":
        recommendations,

        "ai_message":
        message

    }


# ======================================
# AI CEO REPORT ENGINE v1
# ======================================


def get_ceo_report(
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


    orders = (
        db.query(Order)
        .filter(
            Order.tenant_id == tenant_id
        )
        .count()
    )


    products = (
        db.query(Product)
        .filter(
            Product.tenant_id == tenant_id
        )
        .count()
    )


    customers = (
        db.query(Customer)
        .filter(
            Customer.tenant_id == tenant_id
        )
        .count()
    )


    low_stock_items = (
        db.query(Product)
        .join(Inventory)
        .filter(
            Product.tenant_id == tenant_id,
            Inventory.quantity <= Product.reorder_level
        )
        .all()
    )


    low_stock_count = len(low_stock_items)


    estimated_profit = revenue * 0.3


    if revenue > 0 and orders > 0:
        score = 90
        status = "EXPANSION READY"
    elif revenue > 0:
        score = 70
        status = "STABLE"
    else:
        score = 40
        status = "NEEDS SALES"


    if low_stock_count > 0:

        warning = (
            f"⚠️ {low_stock_count} products need restock."
        )

    else:

        warning = (
            "✅ Inventory risk is low."
        )


    if revenue > 0:

        recommendation = [
            "🚀 Increase marketing budget",
            "👥 Improve customer retention",
            "📦 Keep fast moving products available"
        ]

    else:

        recommendation = [
            "📢 Start promotion campaign",
            "🎯 Acquire first customers"
        ]


    return {

        "title":
        "AI CEO Daily Report v3",


        "greeting":
        "👋 Good Morning Owner",


        "business_health":
        {
            "score": score,
            "status": status
        },


        "kpi":
        {
            "revenue": revenue,
            "orders": orders,
            "products": products,
            "customers": customers,
            "estimated_profit": round(
                estimated_profit,
                2
            )
        },


        "inventory_ai":
        {
            "low_stock_count": low_stock_count,
            "warning": warning
        },


        "ai_strategy":
        recommendation,


        "ceo_decision":
        "🚀 Scale business and optimize growth."
    }


# ======================================
# AI SALES FORECAST ENGINE v1
# ======================================

def get_sales_forecast(
    db: Session,
    tenant_id: str
):

    from datetime import datetime, timedelta


    thirty_days_ago = (
        datetime.utcnow()
        -
        timedelta(days=30)
    )


    total_revenue = (
        db.query(
            func.coalesce(
                func.sum(Order.total_amount),
                0
            )
        )
        .filter(
            Order.tenant_id == tenant_id,
            Order.created_at >= thirty_days_ago
        )
        .scalar()
    )


    total_orders = (
        db.query(Order)
        .filter(
            Order.tenant_id == tenant_id,
            Order.created_at >= thirty_days_ago
        )
        .count()
    )


    if total_orders > 0:

        avg_order = (
            total_revenue / total_orders
        )

        forecast = (
            total_revenue * 1.15
        )

        trend = "🟢 Growing"

        advice = (
            "🚀 Sales trend is positive. "
            "Increase marketing and stock availability."
        )

    else:

        avg_order = 0
        forecast = 0

        trend = "⚠️ No sales data"

        advice = (
            "📊 Need more customer activity."
        )


    return {

        "period":
        "Last 30 Days",

        "revenue":
        total_revenue,

        "orders":
        total_orders,

        "average_order_value":
        round(avg_order,2),

        "next_period_forecast":
        round(forecast,2),

        "trend":
        trend,

        "ai_advice":
        advice

    }



# ======================================
# AI TOP PRODUCT INTELLIGENCE ENGINE v1
# ======================================

def get_top_product_intelligence(
    db: Session,
    tenant_id: str
):

    from sqlalchemy import func

    top_product = (
        db.query(
            Product.name,
            func.sum(OrderItem.quantity).label("sold_qty"),
            func.sum(
                OrderItem.quantity * OrderItem.price_at_sale
            ).label("revenue")
        )
        .join(
            OrderItem,
            OrderItem.product_id == Product.id
        )
        .join(
            Order,
            Order.id == OrderItem.order_id
        )
        .filter(
            Product.tenant_id == tenant_id
        )
        .group_by(
            Product.id
        )
        .order_by(
            func.sum(OrderItem.quantity).desc()
        )
        .first()
    )


    if not top_product:

        return {
            "status":"NO_DATA",
            "message":"No sales data available."
        }


    revenue = float(top_product.revenue or 0)


    return {

        "status":"ANALYZED",

        "top_product":{
            "name":top_product.name,
            "units_sold":top_product.sold_qty,
            "revenue":revenue
        },


        "ai_analysis":{

            "performance":
            "🔥 Best selling product detected.",

            "recommendation":
            "Increase stock and promote this product.",

            "growth_action":[

                "🚀 Increase marketing",
                "📦 Maintain inventory",
                "👥 Create customer retention campaign"

            ]

        }

    }



# ======================================
# AI CUSTOMER INTELLIGENCE ENGINE v1
# ======================================


def get_customer_intelligence(
    db: Session,
    tenant_id: str
):

    from datetime import datetime, timedelta
    from src.models.saas_core import Customer
    from src.domains.order.models import Order


    total_customers = (
        db.query(Customer)
        .filter(
            Customer.tenant_id == tenant_id
        )
        .count()
    )


    total_orders = (
        db.query(Order)
        .filter(
            Order.tenant_id == tenant_id
        )
        .count()
    )


    recent_date = (
        datetime.utcnow()
        - timedelta(days=30)
    )


    recent_orders = (
        db.query(Order)
        .filter(
            Order.tenant_id == tenant_id,
            Order.created_at >= recent_date
        )
        .count()
    )


    inactive_customers = max(
        0,
        total_customers - recent_orders
    )


    retention_score = 0

    if total_customers > 0:
        retention_score = min(
            100,
            int(
                (total_orders / total_customers) * 30
            )
        )


    if retention_score >= 70:
        health = "🟢 HEALTHY"
    elif retention_score >= 40:
        health = "🟡 NEED ATTENTION"
    else:
        health = "🔴 AT RISK"


    return {

        "status":
        "ANALYZED",

        "customer_health":
        health,

        "metrics":
        {
            "total_customers": total_customers,
            "total_orders": total_orders,
            "recent_orders_30_days": recent_orders,
            "inactive_customers": inactive_customers
        },

        "retention_score":
        {
            "score": retention_score,
            "status": health
        },

        "ai_insight":
        [
            "👥 Improve customer retention",
            "🎁 Create loyalty rewards",
            "📩 Follow up inactive customers",
            "🚀 Increase repeat purchase rate"
        ],

        "ai_message":
        "Customer growth optimization recommended."
    }



# ======================================
# AI EXECUTIVE DASHBOARD ENGINE v1
# ======================================

def get_ai_dashboard(
    db: Session,
    tenant_id: str
):

    decision = get_ai_decision_engine(
        db,
        tenant_id
    )

    forecast = get_sales_forecast(
        db,
        tenant_id
    )

    top_product = get_top_product_intelligence(
        db,
        tenant_id
    )

    customer = get_customer_intelligence(
        db,
        tenant_id
    )

    ceo = get_ceo_report(
        db,
        tenant_id
    )


    return {

        "business_health":
            {
                "score":
                    decision.get(
                        "business_score",
                        0
                    ),

                "status":
                    decision.get(
                        "status",
                        "UNKNOWN"
                    )
            },


        "revenue":
            {
                "current":
                    forecast.get(
                        "revenue",
                        0
                    ),

                "forecast":
                    forecast.get(
                        "next_period_forecast",
                        0
                    ),

                "trend":
                    forecast.get(
                        "trend",
                        "UNKNOWN"
                    )
            },


        "top_product":
            top_product.get(
                "top_product",
                {}
            ),


        "customer":
            {
                "metrics":
                    customer.get(
                        "metrics",
                        {}
                    ),

                "retention":
                    customer.get(
                        "retention_score",
                        {}
                    )
            },


        "ceo_action":
            ceo.get(
                "ai_strategy",
                []
            ),


        "final_decision":
            ceo.get(
                "ceo_decision",
                "Analyze business"
            )

    }

