import uuid

from sqlalchemy.orm import Session

from src.domains.accounting.services.journal_service import (
    create_purchase_journal,
)

from src.models.saas_core import (
    PurchaseOrder,
    PurchaseItem,
    Supplier,
    SupplierPayable,
)



def create_purchase(
    db: Session,
    tenant_id: str,
    data,
):

    supplier = (
        db.query(Supplier)
        .filter(
            Supplier.id == data.supplier_id,
            Supplier.tenant_id == tenant_id
        )
        .first()
    )

    if not supplier:
        raise Exception("SUPPLIER_NOT_FOUND")


    total = 0


    purchase = PurchaseOrder(
        id=str(uuid.uuid4()),
        purchase_number=data.purchase_number,
        supplier_id=supplier.id,
        total_amount=0,
        status="CONFIRMED",
        tenant_id=tenant_id,
    )


    db.add(purchase)
    db.flush()


    for item in data.items:

        product = (
            db.query(Product)
            .filter(
                Product.id == item.product_id,
                Product.tenant_id == tenant_id
            )
            .first()
        )


        if not product:
            raise Exception("PRODUCT_NOT_FOUND")


        line_total = (
            item.quantity *
            item.unit_cost
        )


        total += line_total


        purchase_item = PurchaseItem(
            id=str(uuid.uuid4()),
            purchase_order_id=purchase.id,
            product_id=product.id,
            quantity=item.quantity,
            unit_cost=item.unit_cost,
            total_cost=line_total,
            tenant_id=tenant_id,
        )


        db.add(purchase_item)


        # STOCK RECEIVE WILL HAPPEN AFTER APPROVAL



    purchase.total_amount = total


    # UPDATE SUPPLIER CURRENT BALANCE
    supplier.current_balance += total


    # SUPPLIER PAYABLE CREATE
    payable = SupplierPayable(
        id=str(uuid.uuid4()),
        purchase_order_id=purchase.id,
        supplier_id=supplier.id,
        total_amount=total,
        paid_amount=0,
        balance_amount=total,
        status="OPEN",
        tenant_id=tenant_id,
    )

    db.add(payable)


    # ACCOUNTING JOURNAL POSTING
    create_purchase_journal(
        db=db,
        tenant_id=tenant_id,
        purchase_id=purchase.id,
        purchase_amount=total,
    )


    db.commit()
    db.refresh(purchase)


    return purchase
