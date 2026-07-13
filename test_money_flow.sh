TOKEN=$(curl -s \
-X POST http://127.0.0.1:8000/api/v4/auth/token \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "username=owner@test.com&password=123456" \
| python -c "import sys,json;print(json.load(sys.stdin)['access_token'])")


echo "===== CREATE RECEIVABLE ====="

curl -s \
-X POST \
http://127.0.0.1:8000/receivables/ \
-H "Authorization: Bearer $TOKEN" \
-H "Content-Type: application/json" \
-d '{
"invoice_id":"38edfba3-c054-42ae-89c4-551ab21ea893",
"customer_id":"cust-test-001"
}' | python -m json.tool


echo

echo "===== CREATE PAYMENT ====="

curl -s \
-X POST \
http://127.0.0.1:8000/payments/ \
-H "Authorization: Bearer $TOKEN" \
-H "Content-Type: application/json" \
-d '{
"payment_number":"PAY-20260712-004",
"invoice_id":"38edfba3-c054-42ae-89c4-551ab21ea893",
"amount":100,
"payment_method":"CASH"
}' | python -m json.tool

