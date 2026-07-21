from pathlib import Path

p = Path("src/domains/dashboard/router.py")
text = p.read_text()

start = text.find('@router.get("/api/v4/dashboard/widgets"')
if start == -1:
    print("NOT FOUND")
    exit()

end = text.find('\n\n@router.', start + 10)

if end == -1:
    end = len(text)

text = text[:start] + text[end:]

p.write_text(text)

print("REMOVED")
