#!/data/data/com.termux/files/usr/bin/bash

sed -i 's|fetch("/products/")|fetch("/api/v4/products")|g' src/templates/products.html
sed -i 's|fetch("/products/",|fetch("/api/v4/products",|g' src/templates/products.html
sed -i 's|window.location.href = "/auth/login"|window.location.href = "/login"|g' src/templates/products.html
sed -i 's|localStorage.getItem("tenant_id")|localStorage.getItem("workspace_id")|g' src/templates/products.html

echo
echo "========== VERIFY =========="
grep -n '/api/v4/products\|workspace_id\|/login' src/templates/products.html
