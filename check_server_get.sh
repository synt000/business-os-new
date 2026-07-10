#!/data/data/com.termux/files/usr/bin/bash

echo "========== ROOT =========="
curl -s http://127.0.0.1:8000/ | head -5

echo
echo "========== DASHBOARD =========="
curl -s http://127.0.0.1:8000/dashboard | head -5

echo
echo "========== PRODUCTS =========="
curl -s http://127.0.0.1:8000/products | head -5
