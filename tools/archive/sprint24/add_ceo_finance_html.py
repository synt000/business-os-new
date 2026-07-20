from pathlib import Path

p = Path("src/templates/dashboard.html")

text = p.read_text()

if 'id="ceoRevenue"' in text and '<!-- CEO FINANCE CARD -->' in text:
    print("Already patched")
    exit()

insert = """

<!-- CEO FINANCE CARD -->

<div class="stat-card">

<div class="stat-icon">
👑
</div>

<div class="stat-number">
<span id="ceoRevenue">
0 MMK
</span>
</div>

<div class="stat-label">
CEO Revenue
</div>

</div>


<div class="stat-card">

<div class="stat-icon">
💎
</div>

<div class="stat-number">
<span id="ceoProfit">
0 MMK
</span>
</div>

<div class="stat-label">
CEO Profit
</div>

</div>


<div class="stat-card">

<div class="stat-icon">
📊
</div>

<div class="stat-number">
<span id="ceoHealth">
0 /100
</span>
</div>

<div class="stat-label">
Finance Health
</div>

</div>


<!-- CEO FINANCE CARD END -->

"""

target = '<div id="stats-container">'

text = text.replace(
    target,
    target + insert
)

p.write_text(text)

print("CEO finance HTML added")
