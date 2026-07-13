echo "===== SEARCH get_current_user ====="
grep -R "Depends(get_current_user)" -n src

echo
echo "===== SEARCH oauth2_scheme ====="
grep -R "oauth2_scheme" -n src

echo
echo "===== SEARCH AuthenticationMiddleware ====="
grep -R "AuthenticationMiddleware" -n src

echo
echo "===== SEARCH BaseHTTPMiddleware ====="
grep -R "BaseHTTPMiddleware" -n src

echo
echo "===== SEARCH orders/ui ====="
grep -R '"/orders/ui"' -n src

echo
echo "===== SEARCH include_router(dashboard_router" 
grep -n "include_router(dashboard_router" -A3 -B3 src/main.py
