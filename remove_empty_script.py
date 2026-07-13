from pathlib import Path

p = Path("src/templates/dashboard.html")
text = p.read_text(encoding="utf-8")

text = text.replace("<script></script>\n", "", 1)
text = text.replace("<script></script>\r\n", "", 1)

p.write_text(text, encoding="utf-8")
print("✅ Removed empty <script></script>")
