from pathlib import Path

p=Path("src/static/js/dashboard_api.js")
s=p.read_text()

old='''new Chart(
            ctx,
            {'''

new='''Chart.register(ChartDataLabels);

        new Chart(
            ctx,
            {'''

if old in s:
    s=s.replace(old,new,1)
    p.write_text(s)
    print("✅ ChartDataLabels registered")
else:
    print("❌ Chart block not found")
