from pathlib import Path

file = Path("src/templates/products.html")

text = file.read_text()

text = text.replace(
    'fetch("/products/", {',
    'fetch("/api/v4/business/products", {'
)

text = text.replace(
    'fetch("/products/")',
    'fetch("/api/v4/business/products")'
)

file.write_text(text)

print("SUCCESS")
print("Products API updated.")
