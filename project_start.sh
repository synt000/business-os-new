#!/data/data/com.termux/files/usr/bin/bash

clear

echo "=========================================="
echo "🚀 BUSINESS OS ENTERPRISE"
echo "=========================================="

echo ""
echo "📅 $(date)"
echo ""

echo "🧠 PROJECT STATUS"
echo "------------------------------------------"

grep "\[x\]" PROJECT_BRAIN.md

echo ""
echo "📋 NEXT TASKS"
echo "------------------------------------------"

grep "\[ \]" TODO.md

echo ""
echo "📝 LAST CHANGE"
echo "------------------------------------------"

tail -5 CHANGELOG.md

echo ""
echo "🌿 GIT STATUS"
echo "------------------------------------------"

git status --short

echo ""

if git diff --quiet && git diff --cached --quiet
then
    echo "✅ Working Tree Clean"
else
    echo "⚠ Uncommitted Changes"
fi

echo ""
echo "=========================================="
echo " Ready To Build Business OS"
echo "=========================================="
