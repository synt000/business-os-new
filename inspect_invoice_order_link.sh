echo "===== INVOICE MODEL ====="
grep -R "class Invoice" -A40 src/models

echo
echo "===== ORDER MODEL ====="
grep -R "class Order" -A50 src/models
