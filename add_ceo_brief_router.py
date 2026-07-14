from pathlib import Path

p = Path("src/domains/ai_insight/router.py")

text = p.read_text(encoding="utf-8")

# import ထည့်
if "generate_ceo_daily_brief" not in text:
    text = text.replace(
        "generate_business_insights",
        "generate_business_insights,\n    generate_ceo_daily_brief"
    )

# endpoint ထည့်
if '"/ceo-brief"' not in text:

    text += '''

@router.get("/ceo-brief")
def ceo_daily_brief(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return generate_ceo_daily_brief(
        db,
        current_user.tenant_id
    )
'''

p.write_text(text, encoding="utf-8")

print("✅ CEO Brief Router Added")
