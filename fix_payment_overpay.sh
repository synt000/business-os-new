cp src/domains/payment/services/payment_service.py src/domains/payment/services/payment_service.py.backup_before_overpay_fix

python - <<'PY'
from pathlib import Path

p = Path("src/domains/payment/services/payment_service.py")

text = p.read_text()

target = '''
    # ==============================
    # CREATE PAYMENT
    # ==============================
'''

insert = '''
    # ==============================
    # OVER PAYMENT PROTECTION
    # ==============================

    from sqlalchemy import func

    paid_total = (
        db.query(func.sum(Payment.amount))
        .filter(
            Payment.invoice_id == invoice.id,
            Payment.status == "COMPLETED"
        )
        .scalar()
        or 0
    )

    remaining = invoice.amount - paid_total

    if data.amount > remaining:
        raise Exception("PAYMENT_EXCEEDS_BALANCE")

'''

if insert.strip() in text:
    print("Already fixed")
elif target in text:
    text=text.replace(target, insert+target)
    p.write_text(text)
    print("✅ Over payment protection added")
else:
    print("Target not found")

PY

grep -n "OVER PAYMENT PROTECTION" -A15 src/domains/payment/services/payment_service.py

