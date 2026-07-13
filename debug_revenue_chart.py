from pathlib import Path

p = Path("src/templates/dashboard.html")
text = p.read_text(encoding="utf-8")

old = 'console.log("Revenue Expense Error",e);'
new = '''
console.log("Revenue Expense Error",e);
alert("Revenue Chart Error: "+e);
'''

text = text.replace(old, new)

p.write_text(text, encoding="utf-8")

print("✅ Revenue Chart Debug Enabled")
