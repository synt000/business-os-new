from pathlib import Path

p = Path("src/templates/dashboard.html")
text = p.read_text(encoding="utf-8")

old = """const data = await res.json();"""

new = """const data = await res.json();

console.log("Profit API:", data);

if(!data.summary){
alert(JSON.stringify(data));
return;
}
"""

text = text.replace(old, new, 1)

p.write_text(text, encoding="utf-8")
print("✅ Profit Debug Added")
