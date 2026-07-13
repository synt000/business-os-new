from pathlib import Path

p = Path("src/domains/dashboard/router.py")
text = p.read_text(encoding="utf-8")

old = """from src.domains.dashboard.service import (
    get_dashboard_menus,
    get_ceo_dashboard_summary,
    get_business_health_score,
)
"""

new = """from src.domains.dashboard.service import (
    get_dashboard_menus,
    get_ceo_dashboard_summary,
    get_business_health_score,
    get_sales_trend,
)
"""

if old in text:
    text = text.replace(old, new)
    p.write_text(text, encoding="utf-8")
    print("✅ get_sales_trend import added")
else:
    print("⚠️ Import block not found. Please check router.py")

