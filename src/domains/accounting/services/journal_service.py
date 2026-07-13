from sqlalchemy.orm import Session

from src.domains.accounting.services.ledger_service import create_ledger_entry


def create_sale_journal(
    db: Session,
    tenant_id: str,
    order_id: str,
    sale_amount: float,
    inventory_cost: float,
):
    """
    Sales Double Entry Journal

    Revenue:
        CREDIT SALES_REVENUE

    Cash:
        DEBIT CASH_ASSET

    COGS:
        DEBIT COGS

    Inventory:
        CREDIT INVENTORY_ASSET
    """

    create_ledger_entry(
        db=db,
        tenant_id=tenant_id,
        entry_type="CREDIT",
        account_head="SALES_REVENUE",
        amount=sale_amount,
        reference_id=order_id,
        description="Sales Revenue",
    )


    create_ledger_entry(
        db=db,
        tenant_id=tenant_id,
        entry_type="DEBIT",
        account_head="CASH_ASSET",
        amount=sale_amount,
        reference_id=order_id,
        description="Customer Payment",
    )


    create_ledger_entry(
        db=db,
        tenant_id=tenant_id,
        entry_type="DEBIT",
        account_head="COGS",
        amount=inventory_cost,
        reference_id=order_id,
        description="Inventory Cost",
    )


    create_ledger_entry(
        db=db,
        tenant_id=tenant_id,
        entry_type="CREDIT",
        account_head="INVENTORY_ASSET",
        amount=inventory_cost,
        reference_id=order_id,
        description="Inventory Out",
    )


    return True
