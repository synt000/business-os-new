#!/data/data/com.termux/files/usr/bin/bash

echo "========== FETCH PRODUCTS BLOCK =========="
grep -n -A60 "async function fetchProducts" src/templates/products.html

echo
echo "========== SUBMIT BLOCK =========="
grep -n -A50 'addEventListener("submit"' src/templates/products.html

echo
echo "========== API RETURN =========="
grep -n '@router.get("/products")' -A20 src/product/router.py
