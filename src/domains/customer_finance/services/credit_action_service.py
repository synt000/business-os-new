from sqlalchemy.orm import Session

from src.domains.customer_finance.services.credit_decision_service import make_credit_decision
from src.domains.customer_finance.services.credit_alert_service import create_credit_alert

from src.models.saas_core import (
    CustomerCreditWallet,
    CustomerCreditActionHistory
)


def apply_credit_decision(db: Session, tenant_id: str, customer_id: str):

    decision = make_credit_decision(
        db=db,
        tenant_id=tenant_id,
        customer_id=customer_id
    )

    wallet = (
        db.query(CustomerCreditWallet)
        .filter(
            CustomerCreditWallet.customer_id == customer_id,
            CustomerCreditWallet.tenant_id == tenant_id
        )
        .first()
    )

    if not wallet:
        raise Exception("WALLET_NOT_FOUND")

    old_limit = wallet.credit_limit

    action = "LIMIT_MAINTAINED"

    if decision["decision"] == "INCREASE_LIMIT":
        wallet.credit_limit = decision["recommended_limit"]
        action = "LIMIT_INCREASED"

    elif decision["decision"] == "REDUCE_LIMIT":
        wallet.credit_limit = decision["recommended_limit"]
        action = "LIMIT_REDUCED"


    db.add(CustomerCreditActionHistory(
        customer_id=customer_id,
        tenant_id=tenant_id,
        action=action,
        old_limit=old_limit,
        new_limit=wallet.credit_limit,
        reason=decision["reason"],
        credit_score=decision["credit_score"],
        behavior_score=decision["behavior_score"]
    ))


    if (
       
        decision["credit_score"] < 60
        or action == "LIMIT_REDUCED"
    ):
        create_credit_alert(
            db=db,
            tenant_id=tenant_id,
            customer_id=customer_id,
            alert_type="HIGH_RISK",
            severity="CRITICAL",
            message="Credit risk requires review"
        )

    db.commit()

    return {
        "customer_id": customer_id,
        "action": action,
        "alert_checked": True
    }
