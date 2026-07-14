#!/data/data/com.termux/files/usr/bin/bash

MESSAGE="$1"

DATE=$(date +"%Y-%m-%d %H:%M")

if [ -z "$MESSAGE" ]; then
    echo "❌ Please add message"
    echo "Example:"
    echo 'bash project_done.sh "Permission UI Completed"'
    exit 1
fi


echo ""
echo "🚀 BUSINESS OS AUTO SAVE"
echo "========================"


echo ""
echo "📝 Updating CHANGELOG..."


cat >> CHANGELOG.md <<EOL

## $DATE

DONE:
- $MESSAGE

EOL


echo "✅ Changelog Updated"



echo ""
echo "💾 Git Backup..."


git add .


git commit -m "DONE: $MESSAGE" 2>/dev/null


if [ $? -eq 0 ]; then
    echo "✅ Git Saved"
else
    echo "⚠️ Git Nothing New"
fi



echo ""
echo "📊 CURRENT STATUS"
echo "================="


grep "\[ \]" TODO.md | head -10


echo ""
echo "================="
echo "✅ AUTO SAVE COMPLETE"
