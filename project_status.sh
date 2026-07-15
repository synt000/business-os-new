#!/data/data/com.termux/files/usr/bin/bash

clear

echo "========================================"
echo "   🚀 BUSINESS OS COMMAND CENTER"
echo "========================================"
echo

echo "📍 CURRENT PHASE"
echo "----------------"
grep "Current Phase" -A6 PROJECT_BRAIN.md 2>/dev/null

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
echo "🌿 GIT STATUS"
echo "-------------"
git status --short

echo
echo "========================================"
