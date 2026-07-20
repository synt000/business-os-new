#!/data/data/com.termux/files/usr/bin/bash

echo "=================================="
echo " BUSINESS OS PROJECT SCAN"
echo "=================================="

echo
echo "[1] Main Structure"
find src -maxdepth 2 -type d | sort

echo
echo "[2] Dashboard"
find src/domains/dashboard -maxdepth 2

echo
echo "[3] Accounting"
find src/domains -maxdepth 2 | grep accounting || true

echo
echo "[4] Finance"
find src/domains -maxdepth 2 | grep finance || true

echo
echo "[5] AI"
find src/domains/ai_insight -maxdepth 2

echo
echo "[6] Purchase"
find src/domains/purchase -maxdepth 2

echo
echo "[7] Payment"
find src/domains/payment -maxdepth 2

echo
echo "[8] Inventory"
find src/domains/inventory -maxdepth 2

echo
echo "[9] Models"
find src/models -maxdepth 1

echo
echo "[10] Services"
find src/services -maxdepth 1

echo
echo "=================================="
echo "END"
echo "=================================="
