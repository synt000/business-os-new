#!/data/data/com.termux/files/usr/bin/bash

echo "=================================="
echo " FINANCE ACCURACY SCAN"
echo "=================================="

echo
echo "===== ACCOUNTING MODELS ====="
nl -ba src/domains/accounting/models.py | sed -n '1,220p'

echo
echo "===== ACCOUNTING SERVICE ====="
nl -ba src/domains/accounting/service.py | sed -n '1,220p'

echo
echo "===== ACCOUNTING SERVICES ====="
find src/domains/accounting/services -type f | sort

echo
echo "===== DASHBOARD FINANCE LOGIC ====="
grep -R "revenue\|profit\|margin\|cash\|payment\|ledger" \
src/domains/dashboard \
--include="*.py"

echo
echo "===== AI FINANCE LOGIC ====="
grep -R "revenue\|profit\|margin\|score\|finance" \
src/domains/ai_insight \
--include="*.py"

echo
echo "===== INVOICE ====="
find src/domains/invoice -maxdepth 2 -type f | sort

echo
echo "===== RECEIVABLE ====="
find src/domains/receivable -maxdepth 2 -type f | sort

echo
echo "=================================="
echo " FINANCE SCAN END"
echo "=================================="

