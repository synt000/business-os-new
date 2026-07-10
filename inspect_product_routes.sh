echo "===== PRODUCT ROUTER ====="
grep -n "@router.get" -A2 src/product/router.py

echo
echo "===== MAIN INCLUDE ====="
grep -n "include_router" src/main.py
