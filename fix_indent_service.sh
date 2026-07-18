#!/data/data/com.termux/files/usr/bin/bash

FILE="src/domains/dashboard/service.py"

cp $FILE ${FILE}.backup_indent_fix

python - <<'PY'
from pathlib import Path

p = Path("src/domains/dashboard/service.py")
s = p.read_text()

# remove misplaced imports inside function
s = s.replace(
"""
    from sqlalchemy import func

from src.domains.product.models import Product
from src.domains.inventory.models import Inventory

    # Revenue
""",
"""
    from sqlalchemy import func

    # Revenue
"""
)

# ensure imports exist at top
if "from src.domains.product.models import Product" not in s.split("def get_finance_insight")[0]:
    s = s.replace(
        "from sqlalchemy import func\n",
        "from sqlalchemy import func\n\nfrom src.domains.product.models import Product\nfrom src.domains.inventory.models import Inventory\n",
        1
    )

p.write_text(s)

print("Indent fixed")
PY

grep -n "from src.domains.product.models" $FILE
grep -n "from src.domains.inventory.models" $FILE

