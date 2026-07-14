from pathlib import Path

p = Path("src/domains/ai_insight/router.py")

text = p.read_text(encoding="utf-8")

if "generate_profit_margin_insight" not in text:

    text = text.replace(
        "from src.domains.ai_insight.service import (\n    generate_business_insights\n)",
        "from src.domains.ai_insight.service import (\n    generate_business_insights,\n    generate_profit_margin_insight\n)"
    )


route = '''

@router.get("/profit-margin")
def profit_margin(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return generate_profit_margin_insight(
        db,
        current_user.tenant_id
    )

'''

if "/profit-margin" not in text:
    text += route

p.write_text(text, encoding="utf-8")

print("✅ Profit Margin API Route Added")
