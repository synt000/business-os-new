echo "===== RECEIVABLE ROUTES ====="
grep -n "@router" -A5 src/domains/receivable/router.py

echo
echo "===== PAYMENT ROUTES ====="
grep -n "@router" -A5 src/domains/payment/router.py
