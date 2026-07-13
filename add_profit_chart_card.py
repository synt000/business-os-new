from pathlib import Path

p = Path("src/templates/dashboard.html")
text = p.read_text(encoding="utf-8")

if "profitChart" in text:
    print("✅ Profit Card Already Exists")
    raise SystemExit

card = '''
<div class="card" style="margin-top:20px;padding:20px;">
<h3>📈 Profit Analysis</h3>
<canvas id="profitChart" height="120"></canvas>
</div>
'''

text = text.replace(
'<canvas id="revenueExpenseChart" height="120"></canvas>\n</div>',
'<canvas id="revenueExpenseChart" height="120"></canvas>\n</div>\n'+card
)

p.write_text(text,encoding="utf-8")

print("✅ Profit Card Added")
