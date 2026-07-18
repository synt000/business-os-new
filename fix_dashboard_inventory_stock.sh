#!/data/data/com.termux/files/usr/bin/bash

FILE="src/domains/dashboard/service.py"

cp $FILE ${FILE}.backup_inventory_stock

python - <<'PY'
from pathlib import Path

p = Path("src/domains/dashboard/service.py")
s = p.read_text()

# Add Inventory import
if "from src.domains.inventory.models import Inventory" not in s:
    s = s.replace(
        "from src.domains.product.models import Product\n",
        "from src.domains.product.models import Product\nfrom src.domains.inventory.models import Inventory\n"
    )

# Replace old stock query
s = s.replace(
    "Product.stock_qty <= Product.low_stock_threshold",
    "Inventory.quantity <= Product.reorder_level"
)

# Add join before filters where needed
s = s.replace(
    "db.query(Product)\n        .filter(\n            Product.tenant_id == tenant_id,\n            Inventory.quantity <= Product.reorder_level",
    "db.query(Product)\n        .join(Inventory)\n        .filter(\n            Product.tenant_id == tenant_id,\n            Inventory.quantity <= Product.reorder_level"
)

p.write_text(s)

print("Inventory stock relation fixed")
PY

grep -n "Inventory\|stock_qty\|reorder_level" $FILE

