#!/data/data/com.termux/files/usr/bin/bash

clear

cd ~/business-os-new || exit

echo "==========================================="
echo "      🚀 BUSINESS OS COMMAND CENTER"
echo "==========================================="
echo

echo "📅 $(date)"
echo

echo "📌 CURRENT PHASE"
echo "----------------"

grep "^## Current Status" -A20 PROJECT_BRAIN.md 2>/dev/null

echo
echo "📋 TODO"
echo "--------"

grep "\[ \]" TODO.md 2>/dev/null

echo
echo "✅ COMPLETED"

grep "\[x\]" TODO.md 2>/dev/null

echo
echo "📝 LAST CHANGE"

tail -5 CHANGELOG.md 2>/dev/null

echo
echo "🌿 GIT STATUS"

git status --short

echo
echo "==========================================="
