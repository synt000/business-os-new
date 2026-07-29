from pathlib import Path

p = Path("src/services/inventory_service.py")

s = p.read_text()

s = s.replace(
    "m.quantity",
    "m.quantity_change"
)

p.write_text(s)

print("✅ InventoryService fixed")
