from pathlib import Path

p = Path(
    "src/domains/order/services/order_service.py"
)

s = p.read_text()

remove = [
    '        print("DEBUG ITEM TYPE:", type(item))',
    '        print("DEBUG ITEM:", item)',
    '        print("DEBUG PRODUCT ID:", product_id)',
    '        print("DEBUG TENANT:", tenant_id)',
    '        print("DEBUG FOUND PRODUCT:", product)',
]

for line in remove:
    s = s.replace(line + "\n", "")


# remove multiline debug blocks
import re

s = re.sub(
    r'\n\s*print\(\n\s*"DEBUG SAME ID COUNT:".*?\n\s*\)\n',
    "\n",
    s,
    flags=re.S
)

s = re.sub(
    r'\n\s*print\(\n\s*"DEBUG TENANT COUNT:".*?\n\s*\)\n',
    "\n",
    s,
    flags=re.S
)


p.write_text(s)

print("✅ order debug cleanup completed")
