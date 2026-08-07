from src.domains.accounting.services.account_resolver import resolve_account


def test_sales_revenue_resolver():
    assert resolve_account("SALE_REVENUE") == "SALES_REVENUE"


def test_cogs_resolver():
    assert resolve_account("COGS_POSTING") == "COGS_EXPENSE"


def test_customer_payment_resolver():
    assert resolve_account("CUSTOMER_PAYMENT") == "CASH_ASSET"


def test_purchase_inventory_resolver():
    assert resolve_account("PURCHASE_INVENTORY") == "INVENTORY_ASSET"


def test_supplier_payment_resolver():
    assert resolve_account("SUPPLIER_PAYMENT") == "SUPPLIER_PAYABLE"


def test_unknown_event_fallback():
    assert resolve_account("UNKNOWN_EVENT") == "CASH_ASSET"
