from sqlalchemy.orm import Session

from src.domains.payment.models import (
    PaymentMethod,
    TenantPaymentMethod,
)


def get_available_payment_methods(
    db: Session,
    tenant_id: str,
):
    return (
        db.query(
            PaymentMethod.code,
            PaymentMethod.name,
            PaymentMethod.category,
            PaymentMethod.ledger_account,
            TenantPaymentMethod.enabled,
            TenantPaymentMethod.is_default,
        )
        .join(
            TenantPaymentMethod,
            TenantPaymentMethod.payment_method_id == PaymentMethod.id,
        )
        .filter(
            TenantPaymentMethod.tenant_id == tenant_id,
            TenantPaymentMethod.enabled == True,
            PaymentMethod.active == True,
        )
        .all()
    )
