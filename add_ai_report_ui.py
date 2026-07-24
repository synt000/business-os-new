from pathlib import Path

p = Path("src/templates/dashboard.html")

s = p.read_text(encoding="utf-8")

block = """

<div class="stat-card" style="margin-bottom:20px;">

<div class="stat-label">
📄 AI CEO Daily Report
</div>

<hr>

<div id="ai_daily_report">
Generating business report...
</div>


<br>

<div class="stat-label">
🔔 Smart Business Alerts
</div>

<div id="ai_alerts">
Checking business risks...
</div>


<br>

<div class="stat-label">
🧠 AI Decision Center
</div>

<div id="ai_decision">
Analyzing best action...
</div>

</div>

"""

if "ai_daily_report" not in s:
    s += block
    print("✅ AI REPORT UI ADDED")
else:
    print("ℹ️ Already exists")

p.write_text(s, encoding="utf-8")
