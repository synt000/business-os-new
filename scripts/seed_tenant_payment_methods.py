from src.core.database import SessionLocal

# Load complete model registry first
import src.models

from src.domains.payment.models import (
    PaymentMethod,
    TenantPaymentMethod,
)


TENANT_ID = "c8f39b5e-2770-42cd-9d13-2ad799337e44"


def seed():
    db = SessionLocal()

    try:
        methods = (
            db.query(PaymentMethod)
            .filter(
                PaymentMethod.code.in_(
                    [
                        "CASH",
                        "KBZ_BANK",
                        "AYA_BANK",
                        "CB_BANK",
                        "CB_ATM",
                        "WAVE_MONEY",
                        "KPAY",
                    ]
                )
            )
            .all()
        )

        for method in methods:

            exists = (
                db.query(TenantPaymentMethod)
                .filter(
                    TenantPaymentMethod.tenant_id == TENANT_ID,
                    TenantPaymentMethod.payment_method_id == method.id,
                )
                .first()
            )

            if exists:
                print("SKIP:", method.code)
                continue

            db.add(
                TenantPaymentMethod(
                    tenant_id=TENANT_ID,
                    payment_method_id=method.id,
                    enabled=True,
                    is_default=(method.code == "CASH"),
                )
            )

            print("ADD:", method.code)

        db.commit()

        print("TENANT PAYMENT METHOD SEED COMPLETE")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed()
