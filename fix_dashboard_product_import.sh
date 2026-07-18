#!/data/data/com.termux/files/usr/bin/bash

FILE="src/domains/dashboard/service.py"

cp $FILE ${FILE}.backup_product_import_final

python - <<'PY'
from pathlib import Path

p = Path("src/domains/dashboard/service.py")
s = p.read_text()

# Remove wrong Product import if exists
s = s.replace(
    "from src.domains.product.models import Product\n\n",
    ""
)

# Add correct import after imports
if "from src.domains.product.models import Product" not in s:
    s = s.replace(
        "from sqlalchemy import func\n",
        "from sqlalchemy import func\n\nfrom src.domains.product.models import Product\n"
    )

# Fix stock query temporarily
s = s.replace(
    "Product.inventory.property.mapper.class_.quantity <= Product.low_stock_threshold",
    "Product.stock_qty <= Product.low_stock_threshold"
)

p.write_text(s)

print("dashboard Product import fixed")
PY

grep -n "from src.domains.product.models import Product" $FILE
grep -n "stock_qty" $FILE

