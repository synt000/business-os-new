from pathlib import Path

p = Path("src/domains/ai_insight/service.py")

text = p.read_text(encoding="utf-8")

if "generate_profit_margin_insight" in text:
    print("✅ Already exists")
    raise SystemExit

add = '''

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
                func.sum(SupplierPayable.amount),
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

'''

text += add

p.write_text(text, encoding="utf-8")

print("✅ Profit Margin AI Added")
