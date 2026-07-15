#!/data/data/com.termux/files/usr/bin/bash

clear

echo "=========================================="
echo "🚀 BUSINESS OS COMMAND CENTER"
echo "=========================================="

echo
echo "📂 Project:"
pwd

echo
echo "🧠 Current Phase"
grep -A10 "## Current Status" PROJECT_BRAIN.md

echo
echo "------------------------------------------"
echo "📋 TODO"
echo "------------------------------------------"
grep "\[ \]" TODO.md

echo
echo "------------------------------------------"
echo "✅ Completed"
echo "------------------------------------------"
grep "\[x\]" TODO.md

echo
echo "------------------------------------------"
echo "📝 Latest Change"
echo "------------------------------------------"
tail -5 CHANGELOG.md

echo
echo "------------------------------------------"
echo "🌿 Git Status"
echo "------------------------------------------"
git status --short

echo
echo "=========================================="
