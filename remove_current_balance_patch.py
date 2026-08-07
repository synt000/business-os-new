from pathlib import Path

path = Path("src/domains/purchase/services/purchase_service.py")

text = path.read_text()

text = text.replace(
    "    # UPDATE SUPPLIER CURRENT BALANCE\n"
    "    supplier.current_balance += total\n",
    ""
)

path.write_text(text)

print("PATCH_DONE")
