#!/data/data/com.termux/files/usr/bin/bash

MESSAGE="$1"

DATE=$(date "+%Y-%m-%d %H:%M")

echo "🚀 BUSINESS OS AUTO SAVE"
echo "========================"

if [ -z "$MESSAGE" ]; then
    echo "❌ Message missing"
    echo "Example:"
    echo "bash project_done.sh \"Permission UI Completed\""
    exit 1
fi


echo ""
echo "📝 Updating CHANGELOG..."

cat >> CHANGELOG.md <<EOL

## $DATE

DONE:
- $MESSAGE

EOL


echo "✅ CHANGELOG Updated"


echo ""
echo "📦 Git Backup..."

git add .

git commit -m "DONE: $MESSAGE"


echo ""
echo "✅ PROJECT SAVED"
echo "================"

git log -1 --oneline
