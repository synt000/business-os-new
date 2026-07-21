from pathlib import Path

p = Path("src/main.py")

text = p.read_text()

backup = Path("src/main.py.before_remove_social_duplicate_v2")
backup.write_text(text)

lines = text.splitlines()

count = 0
output = []

skip_next = False

for line in lines:
    if "from src.domains.social_center.router import router as social_center_router" in line:
        count += 1

        if count == 2:
            skip_next = True
            continue

    if skip_next and "app.include_router(social_center_router)" in line:
        skip_next = False
        continue

    output.append(line)

p.write_text("\n".join(output) + "\n")

print("social_center import count found:", count)

if count >= 2:
    print("✅ Removed second social_center_router include")
else:
    print("❌ Duplicate not found")
