from pathlib import Path

p = Path("src/templates/dashboard.html")
text = p.read_text(encoding="utf-8")

if "aiInsightCard" in text:
    print("✅ AI Insight Card already exists")
    raise SystemExit

block = """
<div id="aiInsightCard" class="card" style="margin-top:20px;padding:20px;">
<h3>🤖 AI Business Insight</h3>
<div id="aiInsightList">
Loading AI Insights...
</div>
</div>
"""

text = text.replace(
    "</body>",
    block + "\n</body>",
    1
)

p.write_text(text, encoding="utf-8")

print("✅ AI Insight Card Added")
