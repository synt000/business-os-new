#!/data/data/com.termux/files/usr/bin/bash

echo "===================================="
echo " PHASE 76D RUNTIME VERIFICATION"
echo "===================================="

BASE="http://127.0.0.1:8000"

echo
echo "[1] Checking /profile ..."
curl -I -s "$BASE/profile"

echo
echo "[2] Checking Dashboard ..."
curl -I -s "$BASE/dashboard"

echo
echo "[3] Checking Products UI ..."
curl -I -s "$BASE/products/ui"

echo
echo "[4] Checking Orders UI ..."
curl -I -s "$BASE/orders/ui"

echo
echo "[5] Checking Inventory UI ..."
curl -I -s "$BASE/inventory/ui"

echo
echo "[6] Checking Reports UI ..."
curl -I -s "$BASE/reports/ui"

echo
echo "===================================="
echo "END OF REPORT"
echo "===================================="
