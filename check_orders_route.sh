echo "===== ORDERS PAGE ROUTE ====="
grep -n "@router.get" -A5 -B2 src/public_page_router.py

echo
grep -R 'orders.html' -n src
