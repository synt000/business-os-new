#!/data/data/com.termux/files/usr/bin/bash

cd ~/business-os-new

python - <<'PY'
from pathlib import Path

p = Path("src/models/saas_core.py")

x = p.read_text()

lines = x.splitlines()

new=[]
skip=False

for line in lines:

    if line.strip().startswith("audit_logs = relationship("):
        skip=True
        continue

    if skip:
        if line.strip()==")":
            skip=False
        continue

    new.append(line)

p.write_text("\n".join(new)+"\n")

print("User audit_logs relationship removed")
PY

