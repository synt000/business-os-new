from pathlib import Path

p = Path("src/templates/dashboard.html")

s = p.read_text()

old = """<h1 class="hero-title">"""

new = """<div id="dashboard-error"
style="
display:none;
margin:15px 0;
padding:12px 16px;
border-radius:12px;
background:#3f1d1d;
color:#ffaaaa;
border:1px solid #ef4444;
font-size:14px;
">
</div>


<h1 class="hero-title">"""

if old in s:
    s=s.replace(old,new,1)
    p.write_text(s)
    print("✅ dashboard error banner added")
else:
    print("❌ hero title marker not found")
