#!/data/data/com.termux/files/usr/bin/bash

if [ -z "$1" ]; then
    echo ""
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

echo "✅ DONE : $TASK"

# ----------------------------------
# CHANGELOG
# ----------------------------------

echo "[$(date '+%Y-%m-%d %H:%M')] $TASK" >> CHANGELOG.md

# ----------------------------------
# TODO AUTO CHECK
# ----------------------------------

if [ -f TODO.md ]; then

FIRST_LINE=$(grep -n "\[ \]" TODO.md | head -1 | cut -d: -f1)

if [ ! -z "$FIRST_LINE" ]; then

sed -i "${FIRST_LINE}s/\[ \]/[x]/" TODO.md

fi

fi

# ----------------------------------
# GIT
# ----------------------------------

git add . >/dev/null 2>&1

git commit -m "DONE: $TASK" >/dev/null 2>&1

echo ""
echo "✔ CHANGELOG Updated"

echo "✔ TODO Updated"

echo "✔ Git Commit Created"

echo ""
echo "-------------"
echo "NEXT TASK"
echo "-------------"

grep "\[ \]" TODO.md

echo ""
echo "-------------"
echo "LAST COMMIT"
echo "-------------"

git log --oneline -1

echo ""

echo "======================================="
