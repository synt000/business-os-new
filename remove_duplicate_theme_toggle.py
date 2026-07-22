from pathlib import Path

p = Path("src/templates/dashboard.html")

lines = p.read_text().splitlines()

found = 0
out = []

skip_block = False

for line in lines:
    if 'id="themeToggle"' in line:
        found += 1
        
        if found == 2:
            continue

    out.append(line)

p.write_text("\n".join(out) + "\n")

print("themeToggle buttons found:", found)
print("duplicate removed if existed")
