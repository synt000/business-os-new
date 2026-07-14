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


def create_purchase_journal(
    db: Session,
    tenant_id: str,
    purchase_id: str,
    purchase_amount: float,
):
    """
    Purchase Double Entry Journal

    Inventory Increase:
        DEBIT INVENTORY_ASSET

    Supplier Liability:
        CREDIT SUPPLIER_PAYABLE
    """

    create_ledger_entry(
        db=db,
        tenant_id=tenant_id,
        entry_type="DEBIT",
        account_head="INVENTORY_ASSET",
        amount=purchase_amount,
        reference_id=purchase_id,
        description="Purchased inventory asset",
    )


    create_ledger_entry(
        db=db,
        tenant_id=tenant_id,
        entry_type="CREDIT",
        account_head="SUPPLIER_PAYABLE",
        amount=purchase_amount,
        reference_id=purchase_id,
        description="Supplier payable created",
    )


    return True

def create_supplier_payment_journal(
    db: Session,
    tenant_id: str,
    payment_id: str,
    payment_amount: float,
):
    """
    Supplier Payment Journal

    Dr Supplier Payable
        Cr Cash Asset
    """

    create_ledger_entry(
        db=db,
        tenant_id=tenant_id,
        entry_type="DEBIT",
        account_head="SUPPLIER_PAYABLE",
        amount=payment_amount,
        reference_id=payment_id,
        description="Supplier payment",
    )

    create_ledger_entry(
        db=db,
        tenant_id=tenant_id,
        entry_type="CREDIT",
        account_head="CASH_ASSET",
        amount=payment_amount,
        reference_id=payment_id,
        description="Cash payment to supplier",
    )

    return True

