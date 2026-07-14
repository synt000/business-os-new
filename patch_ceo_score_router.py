from pathlib import Path

p = Path("src/domains/ai_insight/router.py")

text = p.read_text(encoding="utf-8")

if "generate_ceo_score" not in text:
    text = text.replace(
        "generate_ai_recommendations",
        "generate_ai_recommendations,\n    generate_ceo_score"
    )

if '@router.get("/ceo-score")' not in text:

    text += '''

@router.get("/ceo-score")
def ceo_score(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return generate_ceo_score(
        db,
        current_user.tenant_id
    )
'''

p.write_text(text, encoding="utf-8")

print("CEO Score Router Added")
