#!/data/data/com.termux/files/usr/bin/bash

clear

echo "=========================================="
echo "     🚀 BUSINESS OS COMMAND CENTER"
echo "=========================================="
echo

echo "📅 Today:"
date
echo

echo "📌 CURRENT PHASE"
echo "----------------"
grep "^## Current Status" -A20 PROJECT_BRAIN.md

echo
echo "📋 TODO"
echo "--------"
grep "\[ \]" TODO.md

echo
echo "✅ COMPLETED"
echo "------------"
grep "\[x\]" TODO.md

echo
echo "📝 LAST CHANGE"
echo "--------------"
tail -5 CHANGELOG.md

echo
echo "🌿 Git Status"
echo "-------------"
git status --short

echo
echo "=========================================="
