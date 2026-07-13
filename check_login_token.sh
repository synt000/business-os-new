echo "===== LOGIN HTML ====="
grep -R "access_token" -n src/templates

echo
echo "===== LOGIN JS ====="
grep -R "localStorage.setItem" -n src

echo
echo "===== AUTH LOGIN ====="
grep -R "@router.post" -A30 src/auth

echo
echo "===== ACCESS TOKEN RETURN ====="
grep -R "\"access_token\"" -n src
