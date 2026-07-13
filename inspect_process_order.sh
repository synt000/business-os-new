echo "===== PROCESS ORDER FUNCTION ====="
grep -n '"/orders/"' -A80 -B20 src/templates/orders.html

echo
echo "===== BUTTON ====="
grep -n "Process Order" -A10 -B10 src/templates/orders.html
