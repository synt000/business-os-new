echo "===== verify_access_token ====="
grep -n "def verify_access_token" -A80 src/core/security.py

echo
echo "===== create_access_token ====="
grep -n "def create_access_token" -A80 src/core/security.py

echo
echo "===== LOGIN RETURN ====="
grep -n "access_token" -A20 -B20 src/auth/router.py
