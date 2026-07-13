from pathlib import Path

p = Path("src/domains/dashboard/router.py")
text = p.read_text(encoding="utf-8")

if "get_revenue_expense_summary" not in text:
    text = text.replace(
        "get_sales_trend,",
        "get_sales_trend,\n    get_revenue_expense_summary,"
    )

if '@router.get("/revenue-expense")' not in text:
    api = '''

@router.get("/revenue-expense")
def revenue_expense(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return {
        "status": "SUCCESS",
        "summary": get_revenue_expense_summary(
            db,
            current_user.tenant_id
        )
    }
'''
    text += api

p.write_text(text, encoding="utf-8")
print("✅ Revenue Expense API Added")
