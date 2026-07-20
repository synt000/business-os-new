from pathlib import Path

p = Path("src/main.py")
text = p.read_text(encoding="utf-8")

start = '#@app.middleware("http")'
end = '# REGISTER GLOBAL MIDDLEWARES'

if start in text and end in text:
    before = text.split(start)[0]
    after = text.split(end)[1]
    p.write_text(before + end + after, encoding="utf-8")
    print("✅ Mock auth interceptor removed.")
else:
    print("⚠️ Mock auth block not found.")
