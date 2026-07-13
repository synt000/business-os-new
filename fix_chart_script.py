from pathlib import Path

file = Path("src/templates/dashboard.html")
text = file.read_text(encoding="utf-8")

old = '<script src="https://cdn.jsdelivr.net/npm/chart.js">'
new = '<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>\n\n<script>'

if old in text:
    text = text.replace(old, new, 1)
    file.write_text(text, encoding="utf-8")
    print("✅ Fixed Chart.js script tag")
else:
    print("⚠ Already fixed or tag not found")
