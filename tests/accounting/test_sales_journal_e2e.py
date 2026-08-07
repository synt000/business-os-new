from src.domains.product.models import Product
from src.domains.inventory.models import Inventory
from src.domains.order.services.order_service import create_order
from src.domains.accounting.models import AccountLedger
from src.domains.movement.models import StockMovement


def test_sales_journal_posting(
    db_session,
    tenant_id,
):
    product = Product(
        name="TEST PRODUCT",
        sku="TEST-SKU-001",
        barcode="TEST-BARCODE-001",
        price=100,
        purchase_price=50,
        tenant_id=tenant_id,
    )

    db_session.add(product)
    db_session.flush()

    inventory = Inventory(
        product_id=product.id,
        quantity=10,
        low_stock_threshold=2,
        tenant_id=tenant_id,
    )

    db_session.add(inventory)
    db_session.flush()

    class Item:
        product_id = product.id
        quantity = 2
        price = 100

    order = create_order(
        db=db_session,
        tenant_id=tenant_id,
        order_number="TEST-SALE-001",
        items=[Item()],
        customer_name="Test Customer",
    )

    db_session.flush()

    assert order.id

    movement = (
        db_session.query(StockMovement)
        .filter(
            StockMovement.product_id == product.id
        )
        .first()
    )

    assert movement is not None

    ledger = (
        db_session.query(AccountLedger)
        .filter(
            AccountLedger.reference_id == order.id
        )
        .all()
    )

    heads = {
        x.account_head: x.entry_type
        for x in ledger
    }

    assert heads["SALES_REVENUE"] == "CREDIT"
    assert heads["COGS_EXPENSE"] == "DEBIT"
    assert heads["INVENTORY_ASSET"] == "CREDIT"

from src.domains.accounting.services.journal_service import create_sale_journal


def test_sales_journal_idempotency(
    db_session,
    tenant_id,
):
    from src.domains.accounting.models import AccountLedger

    order_id = "TEST-IDEMPOTENT-SALE-001"

    create_sale_journal(
        db=db_session,
        tenant_id=tenant_id,
        order_id=order_id,
        sale_amount=100,
        inventory_cost=50,
    )

    db_session.flush()

    first_count = (
        db_session.query(AccountLedger)
        .filter(AccountLedger.reference_id == order_id)
        .count()
    )

    create_sale_journal(
        db=db_session,
        tenant_id=tenant_id,
        order_id=order_id,
        sale_amount=100,
        inventory_cost=50,
    )

    db_session.flush()

    second_count = (
        db_session.query(AccountLedger)
        .filter(AccountLedger.reference_id == order_id)
        .count()
    )

    assert first_count == 4
    assert second_count == 4
