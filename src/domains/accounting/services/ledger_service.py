from sqlalchemy.orm import Session

from src.domains.accounting.models import AccountLedger


def create_ledger_entry(
    db: Session,
    tenant_id: str,
    entry_type: str,
    account_head: str,
    amount: float,
    reference_id: str | None = None,
    description: str | None = None,
):
    """
    Enterprise Ledger Entry Creator

    Used by:
    - Sales
    - Purchase
    - Inventory
    - Expense
    - Payroll
    - Banking
    - AI Automation
    """

    entry = AccountLedger(
        tenant_id=tenant_id,
        entry_type=entry_type.upper(),
        account_head=account_head.upper(),
        amount=float(amount),
        reference_id=reference_id,
        description=description,
    )

    db.add(entry)

    return entry
