cp src/domains/order/router.py src/domains/order/router.py.bak

python - <<'PY'
from pathlib import Path

p = Path("src/domains/order/router.py")
text = p.read_text()

old = '''@router.get("/{order_id}")
async def get_order_detail(
'''

new = '''@router.get("/detail/{order_id}")
async def get_order_detail(
'''

if old in text:
    text = text.replace(old, new, 1)

text = text.replace(
    '@router.patch("/{order_id}/status")',
    '@router.patch("/detail/{order_id}/status")'
)

p.write_text(text)

print("✅ Order detail routes moved to /detail/")
PY

echo
echo "===== RESULT ====="
grep -n "@router.get" -A2 src/domains/order/router.py
grep -n "@router.patch" -A2 src/domains/order/router.py
