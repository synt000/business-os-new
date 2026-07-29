from sqlalchemy.orm import Session

from src.domains.accounting.models import AccountLedger


VALID_ENTRY_TYPES = {
    "INCOME",
    "EXPENSE",
}


def check_ledger_integrity(
    db: Session,
    tenant_id: str,
):

    issues = []

    ledgers = (
        db.query(AccountLedger)
        .filter(
            AccountLedger.tenant_id == tenant_id,
        )
        .all()
    )


    for ledger in ledgers:

        # Negative amount check
        if ledger.amount is None or ledger.amount < 0:
            issues.append(
                {
                    "type": "NEGATIVE_LEDGER_AMOUNT",
                    "ledger_id": ledger.id,
                    "amount": ledger.amount,
                }
            )


        # Entry type validation
        if ledger.entry_type not in VALID_ENTRY_TYPES:
            issues.append(
                {
                    "type": "INVALID_ENTRY_TYPE",
                    "ledger_id": ledger.id,
                    "entry_type": ledger.entry_type,
                }
            )


        # Account head validation
        if not ledger.account_head:
            issues.append(
                {
                    "type": "MISSING_ACCOUNT_HEAD",
                    "ledger_id": ledger.id,
                }
            )


    return {
        "status": "OK"
        if not issues else "FAILED",
        "issues": issues,
        "checked_records": len(ledgers),
    }
