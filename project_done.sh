#!/data/data/com.termux/files/usr/bin/bash

if [ -z "$1" ]; then
    echo "Usage:"
    echo './project_done.sh "Task Name"'
    exit 1
fi

TASK="$1"

echo ""
echo "======================================="
echo " BUSINESS OS PROJECT UPDATE"
echo "======================================="
echo ""

echo "✅ DONE: $TASK"

# TODO.md မှာ Task ကို [ ] -> [x] ပြောင်း
if [ -f TODO.md ]; then
    sed -i "s/\[ \] $TASK/[x] $TASK/g" TODO.md
fi

# CHANGELOG
echo "[$(date '+%Y-%m-%d %H:%M')] $TASK" >> CHANGELOG.md

git add . >/dev/null 2>&1
git commit -m "DONE: $TASK" >/dev/null 2>&1

echo ""
echo "✔ TODO Updated"
echo "✔ CHANGELOG Updated"
echo "✔ Git Commit Created"
echo ""

git log --oneline -1

echo ""
echo "======================================="
