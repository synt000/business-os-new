#!/data/data/com.termux/files/usr/bin/bash

clear

echo "========================================"
echo "🚀 BUSINESS OS COMMAND CENTER"
echo "========================================"
echo

echo "📌 CURRENT PHASE"
echo "----------------"
grep -A15 "## Current Status" PROJECT_BRAIN.md 2>/dev/null

echo
echo "📋 TODO"
echo "--------"
grep "\[ \]" TODO.md 2>/dev/null

echo
echo "✅ COMPLETED"
echo "------------"
grep "\[x\]" TODO.md 2>/dev/null

echo
echo "📝 LAST CHANGE"
echo "--------------"
tail -5 CHANGELOG.md 2>/dev/null

echo
echo "🌿 LAST GIT COMMIT"
echo "------------------"
git log --oneline -1

echo
echo "========================================"
