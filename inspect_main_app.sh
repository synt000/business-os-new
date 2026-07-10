#!/data/data/com.termux/files/usr/bin/bash

echo "========== MAIN APP =========="
sed -n '1,220p' src/main.py

echo
echo "========== INCLUDE ROUTERS =========="
grep -n "include_router" src/main.py

echo
echo "========== STATIC FILES =========="
grep -n "StaticFiles" -A3 -B3 src/main.py

echo
echo "========== TEMPLATES =========="
grep -n "Jinja2Templates" -A3 -B3 src/main.py

