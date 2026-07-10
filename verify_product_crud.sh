#!/data/data/com.termux/files/usr/bin/bash

echo "========== ERROR HANDLER =========="
grep -n -A6 "const result" src/templates/products.html

echo
echo "========== FETCH PRODUCTS =========="
grep -n 'fetch("/api/v4/business/products"' src/templates/products.html

echo
echo "========== CATEGORY FETCH =========="
grep -n 'fetch("/api/v4/business/categories"' src/templates/products.html

echo
echo "========== PRODUCT PAYLOAD =========="
grep -n -A10 "const payload" src/templates/products.html

echo
echo "========== PRODUCT API =========="
grep -n '@router.post("/products"' -A20 src/product/router.py

echo
echo "========== PRODUCT GET =========="
grep -n '@router.get("/products")' -A10 src/product/router.py
