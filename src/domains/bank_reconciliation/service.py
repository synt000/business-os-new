from datetime import datetime, timezone

from sqlalchemy.orm import Session

from src.domains.bank_reconciliation.models import BankTransaction
from src.models.saas_core import Payment
from src.domains.audit.service import AuditService


def calculate_match_score(
    bank_transaction,
    payment,
):
    score = 0
    reasons = []

    # amount match
    if float(bank_transaction.amount) == float(payment.amount):
        score += 70
        reasons.append("AMOUNT_MATCH")

    # reference match
    if (
        bank_transaction.external_reference
        and payment.payment_number
        and bank_transaction.external_reference in payment.payment_number
    ):
        score += 20
        reasons.append("REFERENCE_MATCH")

    # date proximity
    if payment.created_at:
        diff = abs(
            (
                bank_transaction.transaction_date -
                payment.created_at
            ).days
        )

        if diff <= 3:
            score += 10
            reasons.append("DATE_CLOSE")

    return score, ",".join(reasons)


def match_bank_transaction(
    db: Session,
    bank_transaction: BankTransaction,
    tenant_id: str,
):

    if bank_transaction.status == "MATCHED":
        return {
            "status": "already_matched",
            "bank_transaction_id": bank_transaction.id,
            "payment_id": bank_transaction.matched_payment_id,
        }


    payments = (
        db.query(Payment)
        .filter(
            Payment.tenant_id == tenant_id,
            Payment.status == "COMPLETED",
        )
        .all()
    )


    scored = []

    for payment in payments:
        score, reason = calculate_match_score(
            bank_transaction,
            payment,
        )

        if score >= 70:
            scored.append(
                (
                    payment,
                    score,
                    reason,
                )
            )


    if len(scored) == 1:

        payment, score, reason = scored[0]

        bank_transaction.matched_payment_id = payment.id
        bank_transaction.status = "MATCHED"
        bank_transaction.match_confidence = score
        bank_transaction.match_reason = reason
        bank_transaction.matched_at = datetime.now(timezone.utc)


        AuditService.create_audit_log(
            db=db,
            tenant_id=tenant_id,
            action="BANK_TRANSACTION_MATCHED",
            table_name="bank_transactions",
            record_id=bank_transaction.id,
            changes=(
                f"Matched {bank_transaction.external_reference} "
                f"to payment {payment.id} "
                f"confidence={score}"
            ),
        )


        db.commit()


        return {
            "status": "matched",
            "confidence": score,
            "reason": reason,
            "bank_transaction_id": bank_transaction.id,
            "payment_id": payment.id,
        }


    if len(scored) > 1:

        bank_transaction.status = "REVIEW"
        db.commit()

        return {
            "status": "review",
            "bank_transaction_id": bank_transaction.id,
        }


    bank_transaction.status = "UNMATCHED"
    db.commit()

    return {
        "status": "unmatched",
        "bank_transaction_id": bank_transaction.id,
    }
