from pathlib import Path

p = Path("src/templates/products.html")
text = p.read_text()

text = text.replace(
"""const products = await response.json();""",
"""const result = await response.json();
const products = result.products || [];"""
)

text = text.replace(
"""price: parseFloat(document.getElementById("price").value),
                    category_id: document.getElementById("category_id").value""",
"""barcode: "",
                    stock_qty: 0,
                    purchase_price: parseFloat(document.getElementById("price").value),
                    retail_price: parseFloat(document.getElementById("price").value)"""
)

text = text.replace(
"${parseFloat(p.price).toFixed(2)}",
"${parseFloat(p.retail_price).toFixed(2)}"
)

p.write_text(text)

print("PRODUCT PAYLOAD PATCHED")
