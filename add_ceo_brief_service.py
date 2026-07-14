from pathlib import Path

p = Path("src/domains/ai_insight/service.py")

text = p.read_text(encoding="utf-8")

if "generate_ceo_daily_brief" not in text:

    text += '''

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

'''

p.write_text(text, encoding="utf-8")

print("✅ CEO Daily Brief Service Added")
