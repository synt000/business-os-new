#!/data/data/com.termux/files/usr/bin/bash

echo "=================================="
echo " Business OS Token Generator"
echo "=================================="

read -p "Username: " USERNAME
read -s -p "Password: " PASSWORD
echo

TOKEN=$(curl -s \
-X POST http://127.0.0.1:8000/api/v4/auth/token \
-H "Content-Type: application/json" \
-d "{\"username\":\"$USERNAME\",\"password\":\"$PASSWORD\"}" \
| python -c "import sys,json; print(json.load(sys.stdin).get('access_token',''))")

if [ -z "$TOKEN" ]; then
    echo
    echo "❌ Login failed."
    exit 1
fi

export ACCESS_TOKEN="$TOKEN"

echo
echo "✅ ACCESS_TOKEN exported successfully."
echo
echo "Test:"
echo 'curl -H "Authorization: Bearer $ACCESS_TOKEN" http://127.0.0.1:8000/dashboard/finance-insight'
echo
echo "Current Token:"
echo "$ACCESS_TOKEN"
