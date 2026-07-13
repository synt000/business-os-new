#!/data/data/com.termux/files/usr/bin/bash

echo "===== Dashboard Function Calls ====="
sed -n '186,215p' src/templates/dashboard.html

echo
echo "===== Search loadProfitChart() ====="
grep -n "loadProfitChart();" src/templates/dashboard.html

echo
echo "===== Search loadRevenueExpense() ====="
grep -n "loadRevenueExpense();" src/templates/dashboard.html

echo
echo "===== Search loadSalesTrend() ====="
grep -n "loadSalesTrend();" src/templates/dashboard.html
