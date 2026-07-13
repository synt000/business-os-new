python - <<'PY'
from pathlib import Path

p=Path("src/templates/orders.html")

s=p.read_text()

s=s.replace(
'${o.customer}',
'${o.customer || "Customer"}'
)

s=s.replace(
'${o.total_usd}',
'${o.total_amount || 0}'
)

p.write_text(s)

print("✅ Orders field mapping fixed")
PY
