from pathlib import Path

p = Path("src/domains/dashboard/router.py")

text = p.read_text()

old = """from src.domains.dashboard.service import (
    get_dashboard_menus,
    get_ceo_dashboard_summary,
    get_business_health_score,
    get_sales_trend,
    get_revenue_expense_summary,
)"""

new = """from src.domains.dashboard.service import (
    get_dashboard_menus,
    get_ceo_dashboard_summary,
    get_business_health_score,
    get_sales_trend,
    get_revenue_expense_summary,
    get_finance_insight,
)"""

if old in text:
    text = text.replace(old, new)
    p.write_text(text)
    print("Finance import added")
else:
    print("Target import block not found")
