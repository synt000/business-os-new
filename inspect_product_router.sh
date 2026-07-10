#!/data/data/com.termux/files/usr/bin/bash

echo "========== PRODUCT ROUTER =========="
sed -n '1,220p' src/product/router.py

echo
echo "========== PRODUCT API ROUTES =========="
grep -n "@router" src/product/router.py
