from sqlalchemy.orm import Session

from src.domains.audit.service import AuditService
from src.domains.payment.models import (
    PaymentMethod,
    TenantPaymentMethod,
)


def enable_payment_method(
    db: Session,
    tenant_id: str,
    payment_code: str,
):
    method = (
        db.query(PaymentMethod)
        .filter(
            PaymentMethod.code == payment_code.upper(),
            PaymentMethod.active == True,
        )
        .first()
    )

    if not method:
        raise Exception("PAYMENT_METHOD_NOT_FOUND")

    mapping = (
        db.query(TenantPaymentMethod)
        .filter(
            TenantPaymentMethod.tenant_id == tenant_id,
            TenantPaymentMethod.payment_method_id == method.id,
        )
        .first()
    )

    if not mapping:
        mapping = TenantPaymentMethod(
            tenant_id=tenant_id,
            payment_method_id=method.id,
            enabled=True,
            is_default=False,
        )
        db.add(mapping)
    else:
        mapping.enabled = True

    db.commit()
    db.refresh(mapping)

    AuditService.create_audit_log(
        db=db,
        tenant_id=tenant_id,
        action="PAYMENT_METHOD_ENABLED",
        table_name="tenant_payment_methods",
        record_id=mapping.id,
    )

    return mapping


def disable_payment_method(
    db: Session,
    tenant_id: str,
    payment_code: str,
):
    method = (
        db.query(PaymentMethod)
        .filter(
            PaymentMethod.code == payment_code.upper()
        )
        .first()
    )

    if not method:
        raise Exception("PAYMENT_METHOD_NOT_FOUND")

    mapping = (
        db.query(TenantPaymentMethod)
        .filter(
            TenantPaymentMethod.tenant_id == tenant_id,
            TenantPaymentMethod.payment_method_id == method.id,
        )
        .first()
    )

    if not mapping:
        raise Exception("TENANT_PAYMENT_METHOD_NOT_FOUND")

    mapping.enabled = False
    mapping.is_default = False

    db.commit()
    db.refresh(mapping)

    AuditService.create_audit_log(
        db=db,
        tenant_id=tenant_id,
        action="PAYMENT_METHOD_DISABLED",
        table_name="tenant_payment_methods",
        record_id=mapping.id,
    )

    return mapping


def set_default_payment_method(
    db: Session,
    tenant_id: str,
    payment_code: str,
):
    method = (
        db.query(PaymentMethod)
        .filter(
            PaymentMethod.code == payment_code.upper(),
            PaymentMethod.active == True,
        )
        .first()
    )

    if not method:
        raise Exception("PAYMENT_METHOD_NOT_FOUND")


    db.query(TenantPaymentMethod).filter(
        TenantPaymentMethod.tenant_id == tenant_id
    ).update(
        {
            TenantPaymentMethod.is_default: False
        }
    )


    mapping = (
        db.query(TenantPaymentMethod)
        .filter(
            TenantPaymentMethod.tenant_id == tenant_id,
            TenantPaymentMethod.payment_method_id == method.id,
        )
        .first()
    )

    if not mapping:
        mapping = TenantPaymentMethod(
            tenant_id=tenant_id,
            payment_method_id=method.id,
            enabled=True,
            is_default=True,
        )
        db.add(mapping)
    else:
        mapping.enabled = True
        mapping.is_default = True

    db.commit()
    db.refresh(mapping)

    AuditService.create_audit_log(
        db=db,
        tenant_id=tenant_id,
        action="PAYMENT_METHOD_DEFAULT_CHANGED",
        table_name="tenant_payment_methods",
        record_id=mapping.id,
    )

    return mapping
