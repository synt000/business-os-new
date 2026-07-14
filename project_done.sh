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

echo ""
echo "[$(date '+%Y-%m-%d %H:%M')] $TASK" >> CHANGELOG.md

git add . >/dev/null 2>&1

git commit -m "DONE: $TASK" >/dev/null 2>&1

echo ""
echo "✔ CHANGELOG Updated"

echo "✔ Git Commit Created"

echo ""

git log --oneline -1

echo ""

echo "======================================="
