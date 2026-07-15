#!/data/data/com.termux/files/usr/bin/bash

clear

echo "=========================================="
echo "      🚀 BUSINESS OS COMMAND CENTER"
echo "=========================================="

echo
echo "📅 $(date)"

echo
echo "🧠 CURRENT PHASE"
grep "^Phase:" PROJECT_BRAIN.md 2>/dev/null

echo
echo "✅ COMPLETED"
grep "\[x\]" PROJECT_BRAIN.md

echo
echo "📋 NEXT TASKS"
grep "\[ \]" TODO.md

echo
echo "📝 LAST CHANGE"
tail -5 CHANGELOG.md

echo
echo "🌿 GIT STATUS"
git status --short

echo
echo "=========================================="
