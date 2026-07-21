from pathlib import Path

p = Path("src/dashboard/router.py")

text = p.read_text()

if '"/api/v4/dashboard/widgets"' in text:
    print("⚠️ widgets already exists")
    exit()

insert_after = """@router.get(
    "/api/v4/dashboard/summary"
)
async def dashboard_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return DashboardService.get_summary(
        db,
        current_user.tenant_id
    )
"""

new_block = """

@router.get("/api/v4/dashboard/widgets")
async def dashboard_widgets(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    today = DashboardService.get_today_stats(
        db,
        current_user.tenant_id
    )

    chart = DashboardService.get_revenue_chart(
        db,
        current_user.tenant_id
    )

    return {
        "today": today,
        "sales_chart": chart,
        "health": {
            "database": "ONLINE",
            "accounting": "ACTIVE",
            "subscription": "ACTIVE",
            "security": "SECURE"
        }
    }
"""

if insert_after in text:
    text = text.replace(
        insert_after,
        insert_after + new_block,
        1
    )
    p.write_text(text)
    print("✅ Added dashboard widgets route")
else:
    print("❌ summary block not found")
