from pathlib import Path

p = Path("src/templates/dashboard.html")

text = p.read_text(encoding="utf-8")

old = """
data.forEach(item=>{

let icon="ℹ️";

if(item.level==="WARNING"){
icon="⚠️";
}

box.innerHTML += `
<div style="margin:12px 0;padding:10px;border-radius:8px;background:#111827;color:white;">
<b>${icon} ${item.title}</b>
<br>
${item.message}
</div>
`;

});
"""

new = """
const insights = Array.isArray(data)
? data
: (data.insights || []);


insights.forEach(item=>{

let icon="ℹ️";

if(item.level==="WARNING"){
icon="⚠️";
}

box.innerHTML += `
<div style="margin:12px 0;padding:10px;border-radius:8px;background:#111827;color:white;">
<b>${icon} ${item.title || "Insight"}</b>
<br>
${item.message || item.action || ""}
</div>
`;

});
"""

if old in text:
    text=text.replace(old,new)
    p.write_text(text,encoding="utf-8")
    print("✅ AI Insight UI Fixed")
else:
    print("⚠ block not found")
