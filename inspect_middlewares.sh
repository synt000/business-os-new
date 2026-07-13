echo "===== MIDDLEWARE ====="
grep -n "SecurityInfrastructureMiddleware" -A40 -B10 src/main.py

echo
echo "===== SECURITY MIDDLEWARE ====="
sed -n '1,260p' src/core/middlewares.py

echo
echo "===== ORDERS UI ====="
grep -n 'orders/ui' -A5 -B5 src/dashboard/router.py
