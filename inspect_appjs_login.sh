#!/data/data/com.termux/files/usr/bin/bash

echo "========== LOGIN FUNCTION =========="
grep -n "async function login" -A80 src/static/app.js || true

echo
echo "========== FETCH CALLS =========="
grep -n "fetch(" -A10 src/static/app.js

echo
echo "========== LOCAL STORAGE =========="
grep -n "localStorage" -A5 -B5 src/static/app.js || true

echo
echo "========== REDIRECT =========="
grep -n "window.location" -A3 -B3 src/static/app.js || true

