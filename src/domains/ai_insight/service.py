from datetime import datetime, time

from sqlalchemy.orm import Session
from src.domains.product.models import Product
from sqlalchemy import func

from src.domains.ai.services.memory_service import save_ai_memory

from src.models.saas_core import (
    Supplier,
    PurchaseOrder,
    PurchaseItem,
    SupplierPayable,
    Customer,
    Order,
    Payment,
    AIInsight,
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

        stock_qty = 0

        if product.inventory:
            stock_qty = product.inventory.quantity

        if stock_qty <= product.reorder_level:

            insights.append({

                "title":
                "Low Stock Alert",

                "message":
                f"{product.name} လက်ကျန် {stock_qty} ခုသာ ကျန်ရှိပါသည်",

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


    save_ai_insights(
        db,
        tenant_id,
        insights
    )

    print("AI MEMORY SYNC START", flush=True)

    for item in insights:

        print("SAVING MEMORY:", item["title"], flush=True)

        save_ai_memory(
            db,
            tenant_id,
            "AI_INSIGHT",
            f"{item['title']}: {item['message']}"
        )

    print("AI MEMORY SYNC DONE", flush=True)

    return insights


# =========================
# PROFIT MARGIN AI ENGINE
# =========================

def generate_profit_margin_insight(
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


    profit = revenue - expense


    margin = 0

    if revenue > 0:
        margin = round(
            (profit / revenue) * 100,
            2
        )


    level = "INFO"

    if margin < 20:
        level = "WARNING"

    elif margin >= 70:
        level = "SUCCESS"


    return {
        "title": "Profit Margin Analysis",
        "revenue": float(revenue),
        "expense": float(expense),
        "profit": float(profit),
        "margin": margin,
        "level": level,
        "message":
            f"Profit Margin {margin}% ဖြစ်ပါသည်"
    }



def generate_ceo_daily_brief(
    db: Session,
    tenant_id: str
):

    profit = generate_profit_margin_insight(
        db,
        tenant_id
    )

    insights = generate_business_insights(
        db,
        tenant_id
    )

    return {
        "title": "CEO Daily Brief",
        "performance": profit,
        "insights": insights[:3]
    }





def generate_ceo_score(
    db: Session,
    tenant_id: str
):

    score = 100

    risks = []

    breakdown = {}


    # =====================
    # INVENTORY HEALTH
    # =====================

    low_stock = 0

    products = (
        db.query(Product)
        .filter(
            Product.tenant_id == tenant_id
        )
        .all()
    )

    for product in products:

        qty = 0

        if product.inventory:
            qty = product.inventory.quantity

        if qty <= product.reorder_level:
            low_stock += 1


    if low_stock > 0:
        inventory_score = 10
        score -= 15

        risks.append(
            "🔴 Low Stock Risk"
        )

    else:
        inventory_score = 20


    breakdown["inventory_health"] = inventory_score



    # =====================
    # CASH FLOW
    # =====================

    debt = (
        db.query(
            func.coalesce(
                func.sum(
                    SupplierPayable.balance_amount
                ),
                0
            )
        )
        .filter(
            SupplierPayable.tenant_id == tenant_id
        )
        .scalar()
    )


    if debt > 0:

        cash_score = 15
        score -= 10

        risks.append(
            "🟡 Supplier Debt Risk"
        )

    else:
        cash_score = 25


    breakdown["cash_flow"] = cash_score



    # =====================
    # SALES HEALTH
    # =====================

    orders = (
        db.query(Order)
        .filter(
            Order.tenant_id == tenant_id
        )
        .count()
    )


    if orders > 0:
        sales_score = 20

    else:
        sales_score = 10


    breakdown["sales_growth"] = sales_score



    # =====================
    # PROFIT HEALTH
    # =====================

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


    if revenue > 0:
        profit_score = 30

    else:
        profit_score = 15


    breakdown["profit_health"] = profit_score



    if score < 0:
        score = 0



    if score >= 80:
        level = "EXCELLENT"

    elif score >= 60:
        level = "WARNING"

    else:
        level = "CRITICAL"



    return {

        "score": score,

        "level": level,

        "breakdown": breakdown,

        "risks": risks,

        "actions": [

            "Create Purchase Order"
            if low_stock > 0
            else "Inventory Stable",

            "Review Supplier Payment Plan"
            if debt > 0
            else "Cash Flow Healthy"

        ]

    }




# ==========================================
# AI CREATE PURCHASE ORDER
# ==========================================

def create_ai_purchase_order(
    db: Session,
    tenant_id: str
):

    product = None

    products = (
        db.query(Product)
        .filter(
            Product.tenant_id == tenant_id
        )
        .all()
    )

    for pdt in products:

        qty = 0

        if pdt.inventory:
            qty = pdt.inventory.quantity

        if qty <= pdt.reorder_level:
            product = pdt
            break


    if not product:
        return {
            "status": "NO_ACTION",
            "message": "Low stock product မရှိပါ"
        }


    supplier = (
        db.query(Supplier)
        .filter(
            Supplier.tenant_id == tenant_id
        )
        .first()
    )


    if not supplier:
        return {
            "status": "FAILED",
            "message": "Supplier မတွေ့ပါ"
        }


    purchase_number = (
        "AI-PO-"
        + datetime.utcnow().strftime("%Y%m%d%H%M%S")
    )


    quantity = 50

    unit_cost = product.purchase_price or 0


    total_cost = quantity * unit_cost


    purchase = PurchaseOrder(

        purchase_number=purchase_number,

        supplier_id=supplier.id,

        total_amount=total_cost,

        status="DRAFT",

        tenant_id=tenant_id

    )


    db.add(purchase)

    db.flush()


    item = PurchaseItem(

        purchase_order_id=purchase.id,

        product_id=product.id,

        quantity=quantity,

        unit_cost=unit_cost,

        total_cost=total_cost,

        tenant_id=tenant_id

    )


    db.add(item)


    payable = SupplierPayable(

        purchase_order_id=purchase.id,

        supplier_id=supplier.id,

        total_amount=total_cost,

        paid_amount=0,

        balance_amount=total_cost,

        status="OPEN",

        tenant_id=tenant_id

    )


    db.add(payable)


    db.commit()


    return {

        "status": "SUCCESS",

        "message": "AI Purchase Order Created",

        "purchase_number": purchase_number,

        "product": product.name,

        "quantity": quantity,

        "amount": total_cost

    }



# =========================
# AI INSIGHT MEMORY SAVE
# =========================

def save_ai_insights(
    db,
    tenant_id,
    insights
):

    try:

        print(
            "🔥 SAVE AI START",
            tenant_id,
            len(insights),
            flush=True
        )

        for item in insights:

            record = AIInsight(
                tenant_id=tenant_id,
                title=item["title"],
                message=item["message"],
                priority=item.get(
                    "level",
                    "NORMAL"
                )
            )

            db.add(record)

        db.commit()

        print(
            "✅ AI INSIGHTS SAVED",
            flush=True
        )

        return True

    except Exception as e:

        db.rollback()

        print(
            "❌ AI SAVE ERROR:",
            repr(e),
            flush=True
        )

        return False

