python - <<'PY'
from pathlib import Path

p = Path("src/templates/orders.html")

s = p.read_text(encoding="utf-8")

old = '''const payload={

platform_channel:"POS",

customer_name:
customer.options[customer.selectedIndex]?.text
||"Walk In Customer",

customer_phone:null,

items:['''

new = '''const payload={

order_number:
"ORD-"+Date.now(),

platform_channel:"POS",

customer_name:
customer.options[customer.selectedIndex]?.text
||"Walk In Customer",

customer_phone:null,

items:['''

if old in s:
    s = s.replace(old,new)
    p.write_text(s,encoding="utf-8")
    print("✅ order_number added")
else:
    print("❌ block not found")
PY
