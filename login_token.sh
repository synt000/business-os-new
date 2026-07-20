#!/data/data/com.termux/files/usr/bin/bash

TOKEN=$(curl -s -X POST http://localhost:8000/api/v4/auth/login \
-H "Content-Type: application/json" \
-d '{"email":"owner@test.com","password":"123456"}' \
| python -c "import sys,json; print(json.load(sys.stdin)['access_token'])")

echo "export TOKEN=\"$TOKEN\"" > .env.token

echo "TOKEN UPDATED"
