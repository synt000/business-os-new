#!/data/data/com.termux/files/usr/bin/bash

cd ~/business-os-new

cp src/domains/audit/models.py \
src/domains/audit/models.py.backup_before_audit_fix

python - <<'PY'
from pathlib import Path

p = Path("src/domains/audit/models.py")

x = p.read_text()

x = x.replace(
'back_populates="audit_logs"',
'back_populates=None'
)

x = x.replace(
'back_populates="user"',
'back_populates=None'
)

x = x.replace(
'back_populates="tenant"',
'back_populates=None'
)

p.write_text(x)

print("Audit back_populates disabled")
PY

