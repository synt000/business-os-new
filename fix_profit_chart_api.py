from pathlib import Path

p = Path("src/templates/dashboard.html")
text = p.read_text(encoding="utf-8")

text = text.replace(
    '"/dashboard/profit-analysis"',
    '"/dashboard/revenue-expense"'
)

p.write_text(text, encoding="utf-8")
print("✅ Profit Chart API fixed")
