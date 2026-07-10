#!/data/data/com.termux/files/usr/bin/bash

echo "========== CATEGORY MODEL =========="
grep -n "class Category" -A25 src/models/saas_core.py

echo
echo "========== PRODUCT MODEL =========="
grep -n "class Product" -A35 src/models/saas_core.py

echo
echo "========== CATEGORY ROUTES =========="
grep -n "@router.get(\"/categories\")" -A15 src/product/router.py

echo
echo "========== PRODUCT TEMPLATE CATEGORY =========="
grep -n "category" src/templates/products.html || true

echo
echo "========== SELECT TAG =========="
grep -n "<select" src/templates/products.html || true
