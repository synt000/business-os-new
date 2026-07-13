echo "===== oauth2_scheme ====="
grep -R "oauth2_scheme" -n src

echo
echo "===== AuthenticationMiddleware ====="
grep -R "AuthenticationMiddleware" -n src

echo
echo "===== include_router(dashboard_router) ====="
grep -n "include_router(dashboard_router" -A5 -B5 src/main.py

echo
echo "===== dashboard router dependency ====="
grep -n "APIRouter(" -A10 src/dashboard/router.py
