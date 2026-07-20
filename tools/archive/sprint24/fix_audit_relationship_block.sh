#!/data/data/com.termux/files/usr/bin/bash

cd ~/business-os-new

cp src/domains/audit/models.py \
src/domains/audit/models.py.backup_before_relationship_block_fix

python - <<'PY'
from pathlib import Path

p = Path("src/domains/audit/models.py")

x = p.read_text()

lines = x.splitlines()

new = []
skip = False

for line in lines:

    if line.strip().startswith("user = relationship("):
        skip = True
        continue

    if line.strip().startswith("tenant = relationship("):
        skip = True
        continue

    if skip:
        if line.strip() == ")":
            skip = False
        continue

    new.append(line)

p.write_text("\n".join(new) + "\n")

print("Audit relationship blocks removed")
PY

