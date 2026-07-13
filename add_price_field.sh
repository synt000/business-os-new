python - <<'PY'
from pathlib import Path

p=Path("src/templates/orders.html")

s=p.read_text(encoding="utf-8")

old='''quantity:
parseInt(
document.getElementById("quantity").value
)

}'''

new='''quantity:
parseInt(
document.getElementById("quantity").value
),

price:
parseFloat(
document.getElementById("price").value
)

}'''

if old in s:
    s=s.replace(old,new)
    p.write_text(s,encoding="utf-8")
    print("✅ price added")
else:
    print("❌ target not found")
PY
