echo "===== INVOICE ====="
sqlite3 business.db "
SELECT invoice_number, amount, status
FROM invoices
WHERE id='38edfba3-c054-42ae-89c4-551ab21ea893';
"

echo
echo "===== RECEIVABLE ====="
sqlite3 business.db "
SELECT invoice_id,total_amount,paid_amount,balance_amount,status
FROM receivables
WHERE invoice_id='38edfba3-c054-42ae-89c4-551ab21ea893';
"

echo
echo "===== PAYMENTS ====="
sqlite3 business.db "
SELECT payment_number,amount,status,invoice_id
FROM payments
WHERE invoice_id='38edfba3-c054-42ae-89c4-551ab21ea893';
"

echo
echo "===== LEDGER ====="
sqlite3 business.db "
SELECT entry_type,account_head,amount,reference_id
FROM account_ledgers
WHERE reference_id='38edfba3-c054-42ae-89c4-551ab21ea893';
"
