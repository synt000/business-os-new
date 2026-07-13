python - <<'PY'
from pathlib import Path

p=Path("src/templates/orders.html")
s=p.read_text()

old="(data.orders||[]).forEach(o=>{"

new="(data.orders || data || []).forEach(o=>{"

if old in s:
    p.write_text(s.replace(old,new))
    print("✅ Orders table array fixed")
else:
    print("❌ not found")
PY
