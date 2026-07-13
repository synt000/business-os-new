echo "===== PRODUCT ROUTES ====="
grep -n "@router" -A3 src/product/router.py

echo
echo "===== PRODUCT API TEST ====="

TOKEN=$(curl -s \
-X POST http://127.0.0.1:8000/api/v4/auth/token \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "username=owner@test.com&password=123456" | python -c "import sys,json;print(json.load(sys.stdin)['access_token'])")

echo
echo "TOKEN OK"

echo
curl -s \
http://127.0.0.1:8000/api/v4/business/products \
-H "Authorization: Bearer $TOKEN" | python -m json.tool

