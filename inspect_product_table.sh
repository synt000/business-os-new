#!/data/data/com.termux/files/usr/bin/bash

echo "========== TABLE HEADER =========="
grep -n -A12 "<thead" src/templates/products.html

echo
echo "========== TABLE ROW =========="
grep -n -A25 "products.forEach" src/templates/products.html
