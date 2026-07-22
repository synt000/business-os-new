from pathlib import Path

p = Path("src/dashboard/router.py")

s = p.read_text()

remove_lines = [
    'print("===== BUSINESS LIST DEBUG =====")',
    'print("==============================")',
    'print("===== DASHBOARD DEBUG =====")',
    'print("==========================")',
]

for x in remove_lines:
    s=s.replace(x,"")

lines=s.splitlines()

result=[]
skip=False

for line in lines:
    if "print(" in line:
        if any(k in line for k in [
            "NAME:",
            "SELECTED:",
            "CURRENT USER:",
            "TENANT:",
            "BUSINESS FOUND:",
            "BUSINESS TYPE:"
        ]):
            skip=True
            continue

    if skip:
        if ")" in line:
            skip=False
        continue

    result.append(line)

p.write_text("\n".join(result))

print("DASHBOARD DEBUG CLEANED")
