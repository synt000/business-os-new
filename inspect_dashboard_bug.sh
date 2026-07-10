#!/data/data/com.termux/files/usr/bin/bash

echo "========== WINDOW ONLOAD =========="
grep -n "window.onload" -A5 -B5 src/static/app.js

echo
echo "========== LOGIN FORM =========="
grep -n 'id="loginForm"' -A20 src/templates/login.html

echo
echo "========== DASHBOARD IDS =========="
grep -n 'id="products"\|id="orders"\|id="customers"\|id="suppliers"' src/templates/dashboard.html

