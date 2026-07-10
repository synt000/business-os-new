#!/data/data/com.termux/files/usr/bin/bash

echo "========== CATEGORY ROUTE =========="
grep -n '@router.get("/categories")' -A5 src/product/router.py

echo
echo "========== START SERVER TEST =========="
curl -s http://127.0.0.1:8000/api/v4/business/categories \
  -H "Authorization: Bearer TEST_TOKEN"

echo
echo
echo "========== CATEGORY SELECT =========="
grep -n -A6 -B2 'id="category_id"' src/templates/products.html

echo
echo "========== loadCategories() =========="
grep -n "loadCategories" -A25 src/templates/products.html
