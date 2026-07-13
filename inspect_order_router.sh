echo "===== ORDER ROUTES ====="
grep -n "@router.get" -A3 -B1 src/domains/order/router.py

echo
echo "===== ORDER PATCH ====="
grep -n "@router.patch" -A3 -B1 src/domains/order/router.py

echo
echo "===== ORDER POST ====="
grep -n "@router.post" -A3 -B1 src/domains/order/router.py
