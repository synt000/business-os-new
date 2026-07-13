python - <<'PY'
from pathlib import Path

p = Path("src/templates/orders.html")

s = p.read_text(encoding="utf-8")

old = """const payload = {

items:[
{
product_id:product.value,
quantity:
parseInt(
document.getElementById("quantity").value
)

}

]

};"""

new = """const payload = {

order_number:
"ORD-"+Date.now(),

items:[
{
product_id:product.value,
quantity:
parseInt(
document.getElementById("quantity").value
)

}

]

};"""

if old not in s:
    print("❌ Payload block not found")
else:
    s = s.replace(old, new)
    p.write_text(s, encoding="utf-8")
    print("✅ Order payload fixed")

PY
