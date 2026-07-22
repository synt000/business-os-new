from pathlib import Path

p = Path("src/templates/dashboard.html")

lines = p.read_text().splitlines()

out = []
skip = False

for i,line in enumerate(lines):

    if '<div class="theme-toggle-wrap">' in line:
        if i > 1680:
            # check broken second block
            nxt = "\n".join(lines[i:i+5])
            if "🌙 Dark" in nxt and 'id="themeToggle"' not in nxt:
                skip = True

    if skip:
        if "</div>" in line:
            skip=False
        continue

    out.append(line)

p.write_text("\n".join(out)+"\n")

print("removed broken theme block")
