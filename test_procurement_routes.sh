echo "===== PROCUREMENT ROUTES ====="
grep -n "procurement" -A5 -B3 src/product/router.py

echo
echo "===== PURCHASE MODULE ====="
find src/domains/purchase -maxdepth 2 -type f
