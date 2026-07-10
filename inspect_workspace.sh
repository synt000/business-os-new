echo "===== workspace.html ====="
grep -n "<script" -A120 src/templates/workspace.html

echo
echo "===== dashboard summary ====="
grep -n "dashboard/summary" -A20 src/templates/workspace.html

echo
echo "===== products element ====="
grep -n 'id="products"' -A2 src/templates/workspace.html

echo
echo "===== app.js ====="
grep -n "loadDashboard\|dashboardSummary\|summary\|products" -A40 src/static/app.js
