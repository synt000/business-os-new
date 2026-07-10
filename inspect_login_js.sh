#!/data/data/com.termux/files/usr/bin/bash

echo "========== LOGIN TEMPLATE (BOTTOM) =========="
tail -n 120 src/templates/login.html

echo
echo "========== SCRIPT TAGS =========="
grep -n "<script" -A120 src/templates/login.html

echo
echo "========== LOCAL STORAGE =========="
grep -n "localStorage" src/templates/login.html || true

echo
echo "========== WINDOW LOCATION =========="
grep -n "window.location" src/templates/login.html || true

