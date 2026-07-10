#!/data/data/com.termux/files/usr/bin/bash

echo "========== SERVER STATUS =========="
curl -I http://127.0.0.1:8000/ 2>/dev/null | head -5

echo
echo "========== DASHBOARD =========="
curl -I http://127.0.0.1:8000/dashboard 2>/dev/null | head -5

echo
echo "========== PRODUCTS PAGE =========="
curl -I http://127.0.0.1:8000/products 2>/dev/null | head -5
