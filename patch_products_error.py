from pathlib import Path

p = Path("src/templates/products.html")
text = p.read_text()

text = text.replace(
'throw new Error(products.detail || "Connection failure.");',
'throw new Error(result.detail || "Connection failure.");'
)

p.write_text(text)

print("ERROR HANDLER PATCHED")
