from pathlib import Path

p = Path("src/domains/ai_insight/service.py")

text = p.read_text(encoding="utf-8")

if "def generate_ceo_score" in text:
    print("Already exists")
    exit()

add = '''

def generate_ceo_score(
    db: Session,
    tenant_id: str
):

    score = 100

    risks = []

    low_stock = (
        db.query(Product)
        .filter(
            Product.tenant_id == tenant_id,
            Product.stock_qty <= Product.low_stock_threshold
        )
        .count()
    )

    if low_stock > 0:
        score -= 15
        risks.append(
            "Low Stock Risk"
        )


    debt = (
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


    if debt > 0:
        score -= 10
        risks.append(
            "Supplier Debt Risk"
        )


    if score < 0:
        score = 0


    return {

        "score": score,

        "level":
        (
            "EXCELLENT"
            if score >= 80
            else
            "WARNING"
        ),

        "risks": risks

    }

'''

p.write_text(
    text + add,
    encoding="utf-8"
)

print("CEO Score Added")
