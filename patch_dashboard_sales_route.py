from pathlib import Path

p = Path("src/domains/dashboard/router.py")
text = p.read_text(encoding="utf-8")

if '@router.get("/sales-trend")' in text:
    print("✅ sales-trend route already exists")
    raise SystemExit

route = '''

@router.get("/sales-trend")
def sales_trend(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return {
        "status": "SUCCESS",
        "trend": get_sales_trend(
            db,
            current_user.tenant_id
        )
    }
'''

text += route

p.write_text(text, encoding="utf-8")

print("✅ sales-trend route added")
