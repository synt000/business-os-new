from pathlib import Path

file = Path("src/models/saas_core.py")

text = file.read_text()

old = '''    procurements = relationship("ProcurementLedger", back_populates="product", cascade="all, delete-orphan")
'''

new = '''    procurements = relationship("ProcurementLedger", back_populates="product", cascade="all, delete-orphan")

    inventory = relationship(
        "Inventory",
        back_populates="product",
        uselist=False
    )
'''

if "inventory = relationship(" in text:
    print("Already fixed")
elif old in text:
    text = text.replace(old, new)
    file.write_text(text)
    print("Product inventory relationship added")
else:
    print("Target line not found")
