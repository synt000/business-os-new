from sqlalchemy.orm import Session

from src.domains.purchase.models import SupplierPayable
from src.models.saas_core import Supplier


def supplier_debt(
    db: Session,
    tenant_id: str
):

    rows = (
        db.query(
            Supplier,
            SupplierPayable
        )
        .join(
            SupplierPayable,
            Supplier.id == SupplierPayable.supplier_id
        )
        .filter(
            SupplierPayable.tenant_id == tenant_id
        )
        .all()
    )


    if not rows:
        return "No supplier debt."


    result = "💰 Supplier Debt\n\n"


    for supplier, payable in rows:

        result += (
            f"{supplier.supplier_name}\n"
            f"Balance: {payable.balance_amount}\n"
            f"Status: {payable.status}\n\n"
        )


    return result
