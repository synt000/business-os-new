echo "===== RECEIVABLE SERVICE ====="
grep -R "def create_receivable" -A80 src/domains/receivable/services

echo
echo "===== RECEIVABLE PAYMENT ====="
grep -R "def payment" -A80 src/domains/receivable/services

echo
echo "===== PAYMENT SERVICE ====="
grep -R "def create_payment" -A80 src/domains/payment/services
