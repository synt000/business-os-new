#!/data/data/com.termux/files/usr/bin/bash

echo "========== LOGIN RESPONSE MODEL =========="
grep -n "class TokenResponseOutboundPayload" -A20 src/auth/router.py

echo
echo "========== LOGIN RETURN =========="
grep -n "return TokenResponseOutboundPayload" -A10 -B10 src/auth/router.py

echo
echo "========== TENANT_ID =========="
grep -n "tenant_id" -A3 -B3 src/auth/router.py

