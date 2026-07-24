from pathlib import Path

p = Path("src/services/dashboard_service.py")

s = p.read_text()

old = '''            "notifications": today["notifications"],
        }
'''

new = '''            "notifications": today["notifications"],

            # Revenue Trend Chart
            "sales_chart": DashboardService.get_revenue_chart(
                db,
                tenant_id
            ),
        }
'''

if old in s:
    s = s.replace(old,new,1)
    print("✅ sales_chart added to summary")
else:
    print("❌ return block not found")

p.write_text(s)
