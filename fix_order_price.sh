python - <<'PY'
from pathlib import Path

p=Path("src/templates/orders.html")
s=p.read_text()

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
    p.write_text(s.replace(old,new))
    print("✅ price field added")
else:
    print("❌ block not found")
PY
