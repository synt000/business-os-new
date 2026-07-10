#!/data/data/com.termux/files/usr/bin/bash

echo "========== GIT VERSION EXISTS =========="

if git cat-file -e HEAD:src/templates/products.html 2>/dev/null; then
    echo "FOUND"
    echo
    echo "========== GIT FILE SIZE =========="
    git show HEAD:src/templates/products.html | wc -l
    echo
    echo "========== FIRST 40 LINES =========="
    git show HEAD:src/templates/products.html | head -40
else
    echo "NOT FOUND"
fi
