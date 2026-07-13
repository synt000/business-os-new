echo "===== CREDIT WALLETS ====="
sqlite3 business.db "
PRAGMA table_info(customer_credit_wallets);
"

echo
echo "===== CREDIT TRANSACTIONS ====="
sqlite3 business.db "
PRAGMA table_info(customer_credit_transactions);
"

echo
echo "===== CREDIT RISK ====="
sqlite3 business.db "
PRAGMA table_info(customer_credit_risk_history);
"

echo
echo "===== CREDIT ALERTS ====="
sqlite3 business.db "
PRAGMA table_info(customer_credit_alerts);
"
