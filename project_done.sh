#!/data/data/com.termux/files/usr/bin/bash

TASK="$1"

DATE=$(date +"%Y-%m-%d")

echo "✅ Saving: $TASK"


echo "" >> CHANGELOG.md

echo "## $DATE" >> CHANGELOG.md

echo "DONE:" >> CHANGELOG.md

echo "- $TASK" >> CHANGELOG.md


echo ""


git add .

git commit -m "DONE: $TASK"


echo "======================"
echo "✅ PROJECT SAVED"
echo "======================"

