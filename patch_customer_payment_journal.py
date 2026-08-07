from pathlib import Path

p = Path("src/domains/customer_payment/service.py")

s = p.read_text()

if "create_customer_payment_journal" in s:
    print("ALREADY PATCHED")
    exit()

s = s.replace(
"from src.domains.audit.service import AuditService",
"""from src.domains.audit.service import AuditService

from src.domains.accounting.services.journal_service import (
    create_customer_payment_journal,
)"""
)


old = """    AuditService.create_audit_log(
        db=db,
        tenant_id=tenant_id,
        action="PAYMENT","""

new = """    create_customer_payment_journal(
        db=db,
        tenant_id=tenant_id,
        payment_id=str(receivable.id),
        payment_amount=data.amount,
    )


    AuditService.create_audit_log(
        db=db,
        tenant_id=tenant_id,
        action="PAYMENT","""

if old not in s:
    print("TARGET NOT FOUND")
else:
    s=s.replace(old,new)
    p.write_text(s)
    print("PATCHED")
