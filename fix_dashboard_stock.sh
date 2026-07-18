#!/data/data/com.termux/files/usr/bin/bash

FILE="src/domains/dashboard/service.py"

echo "=== Backup ==="
cp $FILE ${FILE}.backup_stock_fix

echo "=== Add Product import ==="
python - <<'PY'
from pathlib import Path

p = Path("src/domains/dashboard/service.py")
s = p.read_text()

if "    Product," not in s:
    s = s.replace(
        "    AccountLedger,\n)",
        "    AccountLedger,\n    Product,\n)"
    )

s = s.replace(
    "Product.stock_qty <= Product.low_stock_threshold",
    "Product.inventory.property.mapper.class_.quantity <= Product.low_stock_threshold"
)

p.write_text(s)
print("patched")
PY

echo "=== Verify ==="
grep -n "Product.stock_qty\|Product.inventory.property" $FILE

echo "DONE"
