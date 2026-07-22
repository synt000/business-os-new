from pathlib import Path

p = Path("src/templates/dashboard.html")

s = p.read_text()

s = s.replace(
    'src/static/js/dashboard_api.js?v=5.7',
    'src/static/js/dashboard_api.js?v=5.8'
)

p.write_text(s)

print("dashboard_api version bumped to 5.8")
