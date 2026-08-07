from pathlib import Path

path = Path("src/product/router.py")

text = path.read_text()

old = """class ProductCreateInboundSchema(BaseModel):
    name: str
    sku: str
    barcode: Optional[str] = None
    stock_qty: int = 0
    purchase_price: float = 0.0
    retail_price: float = 0.0
"""

new = """class ProductCreateInboundSchema(BaseModel):
    name: str
    sku: str
    barcode: Optional[str] = None
    stock_qty: int = 0
    purchase_price: float = 0.0
    retail_price: float = 0.0
    description: Optional[str] = None
    brand: Optional[str] = None
    image_url: Optional[str] = None
"""

if old not in text:
    raise SystemExit("TARGET SCHEMA BLOCK NOT FOUND")

path.write_text(text.replace(old, new))

print("✅ ProductCreateInboundSchema attribute fields added")
