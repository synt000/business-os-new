from pathlib import Path

p = Path("src/templates/dashboard.html")

s = p.read_text(encoding="utf-8")

s = s.replace(
'data.dashboard?.today_orders ?? 0;',
'data.dashboard?.total_orders ?? 0;'
)

s = s.replace(
'data.suppliers ?? 0;',
'data.dashboard?.total_suppliers ?? 0;'
)

s = s.replace(
'"$ " + (data.dashboard?.today_revenue ?? 0);',
'"$ " + (data.dashboard?.total_sales ?? 0);'
)

p.write_text(s, encoding="utf-8")

print("✅ Dashboard KPI mapping fixed")
