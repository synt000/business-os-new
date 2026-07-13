echo "===== Orders Route ====="
grep -n '"/api/v4/business/orders"' -A3 -B3 src/templates/orders.html

echo
echo "===== Direct Test ====="

TOKEN=$(curl -s \
-X POST http://127.0.0.1:8000/api/v4/auth/token \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "username=owner@test.com&password=123456" | python -c "import sys,json;print(json.load(sys.stdin)['access_token'])")

echo
echo "Token OK"

echo
curl -i \
http://127.0.0.1:8000/orders/list \
-H "Authorization: Bearer $TOKEN"

echo
echo "===================="

echo
curl -i \
http://127.0.0.1:8000/api/v4/business/orders \
-H "Authorization: Bearer $TOKEN"
