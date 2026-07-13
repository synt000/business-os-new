python - <<'PY'
from pathlib import Path

p=Path("src/templates/orders.html")
s=p.read_text()

old='''toast.innerText=
"✗ "+data.detail;'''

new='''toast.innerText =
"✗ " + (
    Array.isArray(data.detail)
    ? data.detail.map(e => e.msg || JSON.stringify(e)).join("\\n")
    : JSON.stringify(data.detail)
);'''

if old in s:
    p.write_text(s.replace(old,new))
    print("✅ Error display fixed")
else:
    print("❌ Not found")
PY
