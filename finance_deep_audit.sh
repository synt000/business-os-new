#!/data/data/com.termux/files/usr/bin/bash

echo "================================="
echo " FINANCE DEEP AUDIT"
echo "================================="

echo
echo "===== FINANCE SERVICE ====="
nl -ba src/domains/finance/service.py | sed -n '1,220p'

echo
echo "===== ACCOUNTING JOURNAL SERVICE ====="
nl -ba src/domains/accounting/services/journal_service.py | sed -n '1,220p'

echo
echo "===== LEDGER SERVICE ====="
nl -ba src/domains/accounting/services/ledger_service.py | sed -n '1,220p'

echo
echo "===== ACCOUNTING SERVICE ====="
nl -ba src/domains/accounting/services/accounting_service.py | sed -n '1,220p'

echo
echo "===== ORDER MODEL ====="
grep -R "^class Order" -A80 src/domains/order --include="*.py"

echo
echo "===== PURCHASE MODEL ====="
grep -R "^class Purchase" -A100 src/domains/purchase --include="*.py"

echo
echo "===== PAYMENT MODEL ====="
grep -R "^class Payment" -A80 src/models --include="*.py"

echo
echo "================================="
echo " AUDIT END"
echo "================================="

