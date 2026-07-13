from pathlib import Path

p = Path("src/templates/dashboard.html")
text = p.read_text(encoding="utf-8")

block = '''
<div class="card" style="margin-top:20px;padding:20px;">
<h3>💹 Revenue vs Expense</h3>
<canvas id="revenueExpenseChart" height="120"></canvas>
</div>
'''

if "revenueExpenseChart" in text:
    print("✅ Revenue Expense card already exists")
    raise SystemExit

text = text.replace(
    '</div>\n\n<script>',
    block + '\n\n<script>',
    1
)

p.write_text(text, encoding="utf-8")
print("✅ Revenue Expense card added")
