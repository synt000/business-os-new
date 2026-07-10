#!/data/data/com.termux/files/usr/bin/bash

echo "========== RESTORING products.html =========="

git restore src/templates/products.html

echo
echo "========== VERIFY =========="
head -n 20 src/templates/products.html

echo
echo "RESTORE COMPLETE"
