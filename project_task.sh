#!/data/data/com.termux/files/usr/bin/bash

if [ $# -lt 2 ]; then
    echo ""
    echo "Usage:"
    echo "./project_task.sh \"Task Name\" done"
    exit 1
fi

TASK="$1"
STATUS="$2"

if [ "$STATUS" = "done" ]; then

sed -i "s/\[ \] $TASK/[x] $TASK/g" TODO.md 2>/dev/null
sed -i "s/\[ \] $TASK/[x] $TASK/g" PROJECT_BRAIN.md 2>/dev/null

echo "[$(date '+%Y-%m-%d %H:%M')] DONE : $TASK" >> CHANGELOG.md

git add . >/dev/null 2>&1
git commit -m "DONE: $TASK" >/dev/null 2>&1

echo ""
echo "====================================="
echo " BUSINESS OS TASK COMPLETE"
echo "====================================="
echo ""
echo "✅ $TASK"
echo ""
git log --oneline -1
echo ""
echo "====================================="

else
echo "Only supported: done"
fi
