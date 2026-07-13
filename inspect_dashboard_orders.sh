echo "===== DASHBOARD ROUTER ====="
sed -n '90,120p' src/dashboard/router.py

echo
echo "===== ROUTER PREFIX ====="
sed -n '1,25p' src/dashboard/router.py
