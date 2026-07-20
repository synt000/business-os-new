from pathlib import Path

p = Path("src/static/app.js")

text = p.read_text()

dup = '''
    localStorage.setItem(
        "role_profile",
        data.role_profile || ""
    );


'''

text = text.replace(dup, "")

p.write_text(text)

print("✅ duplicate role_profile removed")
