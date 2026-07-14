from pathlib import Path

p = Path("src/domains/ai_insight/service.py")

text = p.read_text(encoding="utf-8")

start = text.index("def generate_ceo_score(")

new_func = '''

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

    low_stock = (
        db.query(Product)
        .filter(
            Product.tenant_id == tenant_id,
            Product.stock_qty <= Product.low_stock_threshold
        )
        .count()
    )


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

'''

text = text[:start] + new_func + "\n"

p.write_text(
    text,
    encoding="utf-8"
)

print("CEO Score Engine Upgraded")
