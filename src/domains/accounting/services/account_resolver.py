"""
Account Identity Resolver

Phase 6.10.30
Business Event -> Ledger Account Mapping

This layer is additive only.
Existing AccountLedger schema remains unchanged.
"""

DEFAULT_ACCOUNT_MAP = {
    "SALE_REVENUE": "SALES_REVENUE",
    "CUSTOMER_PAYMENT": "CASH_ASSET",
    "PURCHASE_INVENTORY": "INVENTORY_ASSET",
    "PURCHASE_PAYABLE": "SUPPLIER_PAYABLE",
    "SUPPLIER_PAYMENT": "SUPPLIER_PAYABLE",
    "COGS_POSTING": "COGS_EXPENSE",
}


def resolve_account(event_code: str) -> str:
    """
    Resolve business event into ledger account identity.

    Future:
    Tenant mapping
    Chart of Accounts mapping
    Database resolver
    """

    code = (event_code or "").upper()

    return DEFAULT_ACCOUNT_MAP.get(
        code,
        "CASH_ASSET"
    )
