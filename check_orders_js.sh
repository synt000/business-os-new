echo "===== ALL FETCH ====="
grep -n "fetch(" -A8 src/templates/orders.html

echo
echo "===== TOKEN ====="
grep -n "const token" -A5 src/templates/orders.html

echo
echo "===== AUTH ====="
grep -n "Authorization" -A2 -B2 src/templates/orders.html

echo
echo "===== LOAD ====="
grep -n "loadOrders" -A30 src/templates/orders.html
