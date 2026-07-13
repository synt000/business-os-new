from pathlib import Path

p = Path("src/domains/dashboard/service.py")
text = p.read_text(encoding="utf-8")

if "def get_revenue_expense_summary(" in text:
    print("✅ Revenue Expense Summary already exists")
    raise SystemExit

code = '''

def get_revenue_expense_summary(
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
                func.sum(SupplierPayable.balance_amount),
                0
            )
        )
        .filter(
            SupplierPayable.tenant_id == tenant_id
        )
        .scalar()
    )

    return {
        "revenue": float(revenue),
        "expense": float(expense),
        "profit": float(revenue - expense)
    }
'''

text += code
p.write_text(text, encoding="utf-8")

print("✅ Revenue Expense Summary Added")
