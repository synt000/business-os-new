#!/data/data/com.termux/files/usr/bin/bash

TOKEN=$(curl -s \
-X POST http://127.0.0.1:8000/api/v4/auth/token \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "username=owner@test.com&password=123456" \
| python -c "import sys,json;print(json.load(sys.stdin)['access_token'])")

export TOKEN

echo "✅ OWNER TOKEN READY"
echo
echo $TOKEN
