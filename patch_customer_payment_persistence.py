from pathlib import Path

p = Path("src/domains/customer_payment/service.py")

s = p.read_text()

if "CustomerPayment" not in s:
    s = s.replace(
        "from src.models.saas_core import (\n    Receivable,\n    Customer,\n)",
        """from src.models.saas_core import (
    Receivable,
    Customer,
)

from src.domains.customer_payment.models import CustomerPayment"""
    )


old = """    create_customer_payment_journal(
        db=db,
        tenant_id=tenant_id,
        payment_id=str(receivable.id),
        payment_amount=data.amount,
    )"""


new = """    payment = CustomerPayment(
        payment_number=data.payment_number,
        customer_id=receivable.customer_id,
        receivable_id=receivable.id,
        amount=data.amount,
        payment_method=data.payment_method,
        status="COMPLETED",
        tenant_id=tenant_id,
    )

    db.add(payment)
    db.flush()


    create_customer_payment_journal(
        db=db,
        tenant_id=tenant_id,
        payment_id=str(payment.id),
        payment_amount=data.amount,
    )"""


if old in s:
    s=s.replace(old,new)


old_return = """        "id": str(uuid.uuid4()),"""

new_return = """        "id": str(payment.id),"""


s=s.replace(old_return,new_return)

p.write_text(s)

print("PATCHED")
