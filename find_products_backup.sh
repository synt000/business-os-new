#!/data/data/com.termux/files/usr/bin/bash

echo "========== FIND PRODUCTS TEMPLATE =========="
find . -name "products.html*" -o -name "*products*"

echo
echo "========== GIT STATUS =========="
git status 2>/dev/null || echo "Not a git repository"

echo
echo "========== GIT LOG =========="
git log --oneline -5 2>/dev/null || true
