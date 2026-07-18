#!/data/data/com.termux/files/usr/bin/bash

FILE="src/domains/dashboard/service.py"

cp $FILE ${FILE}.backup_import_fix

python - <<'PY'
from pathlib import Path

p = Path("src/domains/dashboard/service.py")
s = p.read_text()

# remove wrong import
s = s.replace(
    "    Product,\n",
    ""
)

# add correct import
if "from src.domains.product" not in s:
    s = s.replace(
        "from src.models.saas_core import (",
        "from src.domains.product.models import Product\n\nfrom src.models.saas_core import ("
    )

p.write_text(s)

print("Product import fixed")
PY

grep -n "Product" src/domains/dashboard/service.py

