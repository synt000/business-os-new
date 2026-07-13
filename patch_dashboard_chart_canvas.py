from pathlib import Path

file = Path("src/templates/dashboard.html")
text = file.read_text(encoding="utf-8")

if 'id="salesChart"' in text:
    print("✅ salesChart already exists")
    raise SystemExit

canvas = '''
<div class="card" style="margin-top:20px;padding:20px;">
<h3>📈 Last 7 Days Sales Trend</h3>
<canvas id="salesChart" height="120"></canvas>
</div>

'''

marker = "<script>"

if marker in text:
    text = text.replace(marker, canvas + marker, 1)
    file.write_text(text, encoding="utf-8")
    print("✅ Sales Chart Canvas Added")
else:
    print("❌ <script> tag not found")
