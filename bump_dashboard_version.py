from pathlib import Path

p = Path("src/templates/dashboard.html")

s = p.read_text()

s = s.replace(
    "dashboard.js?v=5.6",
    "dashboard.js?v=5.7"
)

p.write_text(s)

print("version bumped")
