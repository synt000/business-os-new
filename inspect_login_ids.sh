#!/data/data/com.termux/files/usr/bin/bash

echo "========== LOGIN HTML =========="
grep -n 'loginForm\|id="email"\|id="password"\|type="submit"' -A2 -B2 src/templates/login.html

echo
echo "========== APP.JS =========="
grep -n "async function login" -A35 src/static/app.js

echo
echo "========== SCRIPT ORDER =========="
grep -n "<script" -A5 src/templates/login.html

