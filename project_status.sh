#!/data/data/com.termux/files/usr/bin/bash

clear

echo "==============================================="
echo "       🚀 BUSINESS OS COMMAND CENTER"
echo "==============================================="
echo ""

echo "📅 DATE"
date
echo ""

echo "==============================================="
echo "🧠 PROJECT STATUS"
echo "==============================================="

if [ -f PROJECT_BRAIN.md ]; then
cat PROJECT_BRAIN.md
fi

echo ""
echo "==============================================="
echo "📋 TODO"
echo "==============================================="

if [ -f TODO.md ]; then
cat TODO.md
fi

echo ""
echo "==============================================="
echo "📜 CHANGELOG"
echo "==============================================="

if [ -f CHANGELOG.md ]; then
tail -20 CHANGELOG.md
fi

echo ""
echo "==============================================="
echo "🌿 GIT STATUS"
echo "==============================================="

git status --short

echo ""

echo "==============================================="
echo "📝 LAST COMMIT"
echo "==============================================="

git log --oneline -5

echo ""
echo "==============================================="
echo "📊 PROJECT SUMMARY"
echo "==============================================="

DONE=$(grep -R "\[x\]" . --include="TODO.md" 2>/dev/null | wc -l)
TODO=$(grep -R "\[ \]" . --include="TODO.md" 2>/dev/null | wc -l)

echo "✅ Completed : $DONE"
echo "⬜ Remaining : $TODO"

echo ""
echo "==============================================="
echo "READY TO WORK ✅"
echo "==============================================="
