#!/data/data/com.termux/files/usr/bin/bash

clear

echo "=============================================="
echo "      🚀 BUSINESS OS COMMAND CENTER"
echo "=============================================="
echo

echo "📍 PROJECT"
echo "----------------------------------------------"
head -25 PROJECT_BRAIN.md

echo
echo "=============================================="

echo "✅ COMPLETED"
echo "----------------------------------------------"
grep "\[x\]" TODO.md || echo "No completed tasks"

echo
echo "----------------------------------------------"

echo "🟡 REMAINING"
echo "----------------------------------------------"
grep "\[ \]" TODO.md || echo "No remaining tasks"

echo
echo "=============================================="

echo "📝 LAST CHANGES"
echo "----------------------------------------------"
tail -10 CHANGELOG.md

echo
echo "=============================================="

echo "🌿 GIT STATUS"
echo "----------------------------------------------"
git status --short

echo
echo "=============================================="

echo "📌 LAST COMMIT"
echo "----------------------------------------------"
git log --oneline -1

echo
echo "=============================================="
