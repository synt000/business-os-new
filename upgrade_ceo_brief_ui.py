from pathlib import Path

p = Path("src/templates/dashboard.html")

text = p.read_text(encoding="utf-8")

text = text.replace(
'Margin: ${data.performance.margin}%<br><br>',
'''
Margin:
<b>${data.performance.margin}%</b>

<div style="
background:#222;
border-radius:10px;
height:12px;
margin:10px 0;
">

<div style="
width:${data.performance.margin}%;
background:#22c55e;
height:12px;
border-radius:10px;
">
</div>

</div>

<br>
'''
)

text = text.replace(
'''
<b>${i.title}</b><br>
${i.message}
''',
'''
<div style="
padding:10px;
border-radius:8px;
background:${i.level=="WARNING" ? "#7f1d1d" : "#111827"};
margin-bottom:8px;
">

<b>${i.title}</b><br>
${i.message}

</div>
'''
)

p.write_text(text, encoding="utf-8")

print("✅ CEO Brief UI upgraded")
