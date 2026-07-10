#!/data/data/com.termux/files/usr/bin/bash

echo "========== LOGIN PAGE =========="
curl -s http://127.0.0.1:8000/login | head -30

echo
echo "========== AUTH ROUTES =========="
grep -n "@router.post" -A3 src/auth/router.py

echo
echo "========== LOGIN FETCH =========="
grep -n "fetch(" src/templates/login.html || true

echo
echo "========== ACCESS TOKEN =========="
grep -n "access_token" -A5 -B5 src/templates/login.html || true

