from pathlib import Path

p = Path("src/domains/product/models.py")

s = p.read_text()

s = s.replace(
'''    # order_items relationship disabled
    # Legacy saas_core OrderItem isolation fix

    # procurements relationship disabled
    # Legacy ProcurementLedger isolation fix
''',
'''    order_items = relationship(
        "OrderItem",
        back_populates="product",
        cascade="all, delete-orphan"
    )

    procurements = relationship(
        "ProcurementLedger",
        back_populates="product"
    )
'''
)

p.write_text(s)

print("✅ Product relationships restored")
