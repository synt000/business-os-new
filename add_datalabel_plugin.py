from pathlib import Path

p = Path("src/templates/dashboard.html")
s = p.read_text()

old = '<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>'

new = '''<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels"></script>'''

if old in s:
    s=s.replace(old,new,1)
    p.write_text(s)
    print("✅ datalabel plugin added")
else:
    print("❌ chart CDN not found")
