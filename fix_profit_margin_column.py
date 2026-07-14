from pathlib import Path

p = Path("src/domains/ai_insight/service.py")

text = p.read_text(encoding="utf-8")

text = text.replace(
    "func.sum(SupplierPayable.amount)",
    "func.sum(SupplierPayable.balance_amount)"
)

p.write_text(text, encoding="utf-8")

print("✅ Fixed SupplierPayable column")
