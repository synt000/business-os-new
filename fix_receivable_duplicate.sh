cp src/domains/receivable/router.py src/domains/receivable/router.py.backup_before_duplicate_fix

python - <<'PY'
from pathlib import Path

p = Path("src/domains/receivable/router.py")

text = p.read_text()

old = '''    if not invoice:
        raise HTTPException(
            status_code=404,
            detail="INVOICE_NOT_FOUND"
        )

    receivable = create_receivable(
'''

new = '''    if not invoice:
        raise HTTPException(
            status_code=404,
            detail="INVOICE_NOT_FOUND"
        )

    # ==============================
    # DUPLICATE RECEIVABLE CHECK
    # ==============================
    existing = (
        db.query(Receivable)
        .filter(
            Receivable.invoice_id == invoice.id
        )
        .first()
    )

    if existing:
        return existing

    receivable = create_receivable(
'''

if old not in text:
    print("❌ Target block not found")
else:
    text = text.replace(old, new)
    p.write_text(text)
    print("✅ Receivable duplicate guard added")

PY

echo
echo "===== VERIFY ====="
grep -n "DUPLICATE RECEIVABLE CHECK" -A15 src/domains/receivable/router.py

