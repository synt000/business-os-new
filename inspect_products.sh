echo "===== PRODUCT ROUTES ====="
grep -n "@router.post\|@router.get\|@router.put\|@router.delete" -A2 src/product/router.py

echo
echo "===== PRODUCT TEMPLATE ====="
sed -n '1,220p' src/templates/products.html
