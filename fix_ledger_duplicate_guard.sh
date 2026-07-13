cp src/domains/payment/services/payment_service.py \
src/domains/payment/services/payment_service.py.backup_before_ledger_guard

python - <<'PY'
from pathlib import Path

p = Path("src/domains/payment/services/payment_service.py")

text = p.read_text()

old = '''
    ledger = AccountLedger(
        entry_type="INCOME",
        account_head="SALES_PAYMENT",
        amount=data.amount,
        reference_id=invoice.id,
        description=f"Payment received {data.payment_number}",
        tenant_id=tenant_id,
    )
'''

new = '''
    # ==============================
    # LEDGER DUPLICATE PROTECTION
    # ==============================

    existing_ledger = (
        db.query(AccountLedger)
        .filter(
            AccountLedger.reference_id == invoice.id,
            AccountLedger.account_head == "SALES_PAYMENT",
            AccountLedger.tenant_id == tenant_id,
        )
        .first()
    )

    ledger = None

    if not existing_ledger:
        ledger = AccountLedger(
            entry_type="INCOME",
            account_head="SALES_PAYMENT",
            amount=data.amount,
            reference_id=invoice.id,
            description=f"Payment received {data.payment_number}",
            tenant_id=tenant_id,
        )
'''

if old not in text:
    print("❌ Ledger block not found")
else:
    text=text.replace(old,new)
    p.write_text(text)
    print("✅ Ledger duplicate guard added")

PY

grep -n "LEDGER DUPLICATE PROTECTION" -A25 src/domains/payment/services/payment_service.py

