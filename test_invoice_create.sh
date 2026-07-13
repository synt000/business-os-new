TOKEN=$(curl -s \
-X POST http://127.0.0.1:8000/api/v4/auth/token \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "username=owner@test.com&password=123456" \
| python -c "import sys,json;print(json.load(sys.stdin)['access_token'])")

echo "===== CREATE INVOICE TEST ====="

curl -s \
-X POST \
http://127.0.0.1:8000/invoices/ \
-H "Authorization: Bearer $TOKEN" \
-H "Content-Type: application/json" \
-d '{
    "order_id":"75989c91-f6ef-4062-a25c-0ed50008d286",
    "invoice_number":"INV-20260712-001"
}' \
| python -m json.tool
