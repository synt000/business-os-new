from pathlib import Path

p = Path("src/templates/dashboard.html")

text = p.read_text()

old = '"/owner/ceo-summary"'

if old in text:
    text = text.replace(
        old,
        '"/api/v4/dashboard/summary"',
        1
    )
    p.write_text(text)
    print("DONE")
else:
    print("NOT FOUND")
