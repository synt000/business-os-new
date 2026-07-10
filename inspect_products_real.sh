#!/data/data/com.termux/files/usr/bin/bash

echo "========== FILE INFO =========="
ls -lh src/templates/products.html

echo
echo "========== FIRST 60 LINES =========="
head -n 60 src/templates/products.html

echo
echo "========== LAST 40 LINES =========="
tail -n 40 src/templates/products.html
