from pathlib import Path

p = Path("src/templates/login.html")
text = p.read_text()

# remove duplicate appended script
parts = text.split("</html>")

if len(parts) > 1:
    body = parts[0] + "</html>"
else:
    body = text

p.write_text(body)

print("LOGIN HTML CLEANED")
