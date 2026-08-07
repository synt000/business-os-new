from sqlalchemy.orm import Session

from src.domains.payment.models import (
    PaymentMethod,
    TenantPaymentMethod,
)


def resolve_payment_account(
    db: Session,
    tenant_id: str,
    payment_method: str,
) -> str:
    """
    Configuration-driven payment account resolver.

    Phase 6.5:
    Database configuration first.
    Static fallback preserved.
    """

    code = (payment_method or "").upper()

    # =====================================
    # DATABASE CONFIGURATION PATH
    # =====================================

    result = (
        db.query(PaymentMethod.ledger_account)
        .join(
            TenantPaymentMethod,
            TenantPaymentMethod.payment_method_id == PaymentMethod.id,
        )
        .filter(
            TenantPaymentMethod.tenant_id == tenant_id,
            TenantPaymentMethod.enabled == True,
            PaymentMethod.code == code,
            PaymentMethod.active == True,
        )
        .first()
    )

    if result:
        return result[0]


    # =====================================
    # STATIC FALLBACK (PROTECTED)
    # =====================================

    fallback = {
        "CASH": "CASH_ASSET",
        "BANK": "BANK_ASSET",
        "BANK_TRANSFER": "BANK_ASSET",
        "KBZ_BANK": "BANK_ASSET",
        "AYA_BANK": "BANK_ASSET",
        "CB_BANK": "BANK_ASSET",
        "CB_ATM": "BANK_ASSET",
        "WALLET": "DIGITAL_ASSET",
        "WAVE_MONEY": "DIGITAL_ASSET",
        "KPAY": "DIGITAL_ASSET",
        "CARD": "BANK_ASSET",
    }

    return fallback.get(
        code,
        "CASH_ASSET",
    )
