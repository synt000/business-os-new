#!/data/data/com.termux/files/usr/bin/bash

if [ -z "$1" ]; then
    echo "Usage:"
    echo "./project_done.sh \"Completed Task\""
    exit 1
fi

TASK="$1"

echo ""
echo "======================================="
echo " BUSINESS OS PROJECT UPDATE"
echo "======================================="
echo ""

echo "✅ DONE: $TASK"

# ----------------------------
# Auto Update TODO.md
# ----------------------------
if [ -f TODO.md ]; then
python - "$TASK" <<'PY'
import sys
from pathlib import Path

task = sys.argv[1]
todo = Path("TODO.md")

text = todo.read_text(encoding="utf-8")

lines = text.splitlines()
new = []

for line in lines:
    if "[ ]" in line and task.lower() in line.lower():
        line = line.replace("[ ]","[x]",1)
    new.append(line)

todo.write_text("\n".join(new),encoding="utf-8")
PY
fi

# ----------------------------
# Update CHANGELOG
# ----------------------------
echo "[$(date '+%Y-%m-%d %H:%M')] $TASK" >> CHANGELOG.md

# ----------------------------
# Git
# ----------------------------
git add . >/dev/null 2>&1
git commit -m "DONE: $TASK" >/dev/null 2>&1

echo ""
echo "✔ TODO Updated"
echo "✔ CHANGELOG Updated"
echo "✔ Git Commit Created"

echo ""
git log --oneline -1

echo ""
echo "--------------- TODO STATUS ---------------"

if [ -f TODO.md ]; then
grep "\[ \]" TODO.md || echo "🎉 ALL TASKS COMPLETED"
fi

echo ""
echo "======================================="
