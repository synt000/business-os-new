#!/data/data/com.termux/files/usr/bin/bash

MESSAGE="$1"

DATE=$(date +"%Y-%m-%d")

echo "🚀 BUSINESS OS AUTO SAVE"

echo ""

if [ -z "$MESSAGE" ]; then
    echo "Usage:"
    echo "bash project_done.sh \"Task Completed\""
    exit 1
fi


echo "✅ Updating CHANGELOG..."

cat >> CHANGELOG.md <<EOL

## $DATE

DONE:
- $MESSAGE

EOL


echo "✅ Git Backup..."

git add .

git commit -m "DONE: $MESSAGE" 2>/dev/null


echo ""
echo "======================"
echo "✅ SAVED:"
echo "$MESSAGE"
echo "======================"
