from pathlib import Path

p = Path("src/models/saas_core.py")

text = p.read_text()

old = """    stock_qty = Column(Integer, default=0)
    purchase_price = Column(Float, default=0.0)
    retail_price = Column(Float, default=0.0)
"""

new = """    stock_qty = Column(Integer, default=0)
    low_stock_threshold = Column(Integer, default=10)
    purchase_price = Column(Float, default=0.0)
    retail_price = Column(Float, default=0.0)
"""

if "low_stock_threshold" not in text:
    text = text.replace(old, new)
    p.write_text(text)
    print("LOW STOCK COLUMN ADDED")
else:
    print("ALREADY EXISTS")
