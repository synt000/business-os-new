from pathlib import Path

p = Path("src/templates/dashboard.html")
text = p.read_text(encoding="utf-8")

if "https://cdn.jsdelivr.net/npm/chart.js" in text:
    print("✅ Chart.js already installed")
    raise SystemExit

text = text.replace(
    "</head>",
    '    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>\n</head>'
)

p.write_text(text, encoding="utf-8")

print("✅ Chart.js added")
