TOKEN=$(curl -s \
-X POST http://127.0.0.1:8000/api/v4/auth/token \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "username=owner@test.com&password=123456" \
| python -c "import sys,json;print(json.load(sys.stdin)['access_token'])")


echo "===== BEFORE STOCK ====="

curl -s \
http://127.0.0.1:8000/api/v4/business/products \
-H "Authorization: Bearer $TOKEN" \
| python -m json.tool


echo
echo "===== CREATE PROCUREMENT ====="


curl -s -X POST \
http://127.0.0.1:8000/api/v4/business/procurements \
-H "Authorization: Bearer $TOKEN" \
-H "Content-Type: application/json" \
-d '{
"product_id":"4a863700-026d-4d2f-b907-f6984c2da9ce",
"supplier_id":"36133e67-bd3b-48dc-b4d7-db5e84257802",
"qty_purchased":20,
"unit_cost":500
}' \
| python -m json.tool


echo
echo "===== AFTER STOCK ====="

curl -s \
http://127.0.0.1:8000/api/v4/business/products \
-H "Authorization: Bearer $TOKEN" \
| python -m json.tool

