from pathlib import Path

p = Path("src/domains/ai_insight/router.py")

text = p.read_text(encoding="utf-8")

text = text.replace(
"""    return generate_business_insights,
    generate_ceo_daily_brief(
        db,
        current_user.tenant_id
    )
""",
"""    return generate_business_insights(
        db,
        current_user.tenant_id
    )
"""
)

text = text.replace(
"""    return generate_ai_recommendations,
    generate_ceo_score(
        db,
        current_user.tenant_id
    )
""",
"""    return generate_ai_recommendations(
        db,
        current_user.tenant_id
    )
"""
)

p.write_text(text, encoding="utf-8")

print("✅ Fixed AI Router Returns")
