echo "===== BUSINESS ORDER ROUTES ====="
grep -R '"/api/v4/business/orders' -n src

echo
echo "===== ORDER ROUTER PREFIX ====="
grep -n "APIRouter(" -A5 src/domains/order/router.py

echo
echo "===== BUSINESS ROUTER ====="
grep -R "business/orders" -n src | grep router
