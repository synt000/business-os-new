from pathlib import Path

p = Path("src/templates/dashboard.html")

text = p.read_text()

if 'id="restock_modal"' in text:
    print("⚠️ AI Modal already exists")
    exit()

insert = r'''

<!-- SMART RESTOCK MODAL -->

<div id="restock_modal"
style="
display:none;
position:fixed;
top:0;
left:0;
width:100%;
height:100%;
background:rgba(0,0,0,.65);
z-index:9999;
">

<div style="
background:#111827;
color:white;
margin:12% auto;
padding:25px;
width:85%;
border-radius:20px;
">

<h3>📦 Smart Restock AI</h3>

<hr>

<div id="restock_content">
Loading...
</div>

<br>

<button onclick="closeRestockModal()"
style="
width:100%;
padding:12px;
border:none;
border-radius:12px;
background:#ef4444;
color:white;
">
Close
</button>

</div>
</div>


<!-- CEO REPORT MODAL -->

<div id="ceo_modal"
style="
display:none;
position:fixed;
top:0;
left:0;
width:100%;
height:100%;
background:rgba(0,0,0,.65);
z-index:9999;
">

<div style="
background:#111827;
color:white;
margin:12% auto;
padding:25px;
width:85%;
border-radius:20px;
">

<h3>📊 AI CEO Daily Report</h3>

<hr>

<div id="ceo_content">
Loading...
</div>

<br>

<button onclick="closeCEOReport()"
style="
width:100%;
padding:12px;
border:none;
border-radius:12px;
background:#ef4444;
color:white;
">
Close
</button>

</div>
</div>

'''

pos = text.rfind("</body>")

if pos == -1:
    print("❌ </body> not found")
else:
    text = text[:pos] + insert + text[pos:]
    p.write_text(text)
    print("✅ AI Modals inserted")

