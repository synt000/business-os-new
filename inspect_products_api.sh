#!/data/data/com.termux/files/usr/bin/bash

echo "========== FETCH CALLS =========="
grep -n "fetch(" src/templates/products.html || true

echo
echo "========== OLD PRODUCT API =========="
grep -n "/api/v4/products" src/templates/products.html || true

echo
echo "========== NEW BUSINESS API =========="
grep -n "/api/v4/business/products" src/templates/products.html || true

echo
echo "========== CATEGORY API =========="
grep -n "/categories" src/templates/products.html || true

echo
echo "========== TOKEN =========="
grep -n "Authorization" src/templates/products.html || true

echo
echo "========== LOCAL STORAGE =========="
grep -n "localStorage" src/templates/products.html || true

