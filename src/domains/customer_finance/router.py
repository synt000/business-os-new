from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.security import get_current_user

from src.domains.customer_finance.services.customer_balance_service import (
    get_customer_balance
)

from src.domains.customer_finance.services.customer_statement_service import (
    get_customer_statement
)

from src.domains.customer_finance.services.credit_analytics_service import (
    get_credit_summary,
)

from src.domains.customer_finance.services.credit_wallet_service import (
    get_credit_wallet,
    get_credit_history,
    topup_credit,
    refund_credit,
    update_credit_limit,
    use_credit_for_invoice
)


router = APIRouter(
    prefix="/customer-finance",
    tags=["Customer Finance"]
)


@router.get("/{customer_id}/balance")
def customer_balance(
    customer_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_customer_balance(
        db,
        current_user.tenant_id,
        customer_id
    )


@router.get("/{customer_id}/statement")
def customer_statement(
    customer_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_customer_statement(
        db,
        current_user.tenant_id,
        customer_id
    )


@router.get("/{customer_id}/credit")
def customer_credit(
    customer_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_credit_wallet(
        db,
        current_user.tenant_id,
        customer_id
    )


@router.post("/{customer_id}/credit/use")
def use_customer_credit(
    customer_id: str,
    invoice_id: str,
    amount: float,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return use_credit_for_invoice(
        db,
        current_user.tenant_id,
        customer_id,
        invoice_id,
        amount
    )


@router.get("/{customer_id}/credit/history")
def customer_credit_history(
    customer_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_credit_history(
        db,
        current_user.tenant_id,
        customer_id
    )


@router.post("/{customer_id}/credit/topup")
def customer_credit_topup(
    customer_id: str,
    amount: float,
    notes: str = "Manual credit top-up",
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return topup_credit(
        db=db,
        tenant_id=current_user.tenant_id,
        customer_id=customer_id,
        amount=amount,
        notes=notes
    )


@router.post("/{customer_id}/credit/refund")
def customer_credit_refund(
    customer_id: str,
    amount: float,
    invoice_id: str | None = None,
    notes: str = "Credit refund",
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return refund_credit(
        db=db,
        tenant_id=current_user.tenant_id,
       
        customer_id=customer_id,
        amount=amount,
        invoice_id=invoice_id,
        notes=notes
    )



@router.patch("/{customer_id}/credit-limit")
def update_customer_credit_limit(
    customer_id: str,
    credit_limit: float,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return update_credit_limit(
        db=db,
        tenant_id=current_user.tenant_id,
        customer_id=customer_id,
        credit_limit=credit_limit
    )


@router.get("/analytics/credit-summary")
def credit_summary_analytics(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_credit_summary(
        db=db,
        tenant_id=current_user.tenant_id
    )


from src.domains.customer_finance.services.credit_risk_service import (
    calculate_customer_credit_score
)


@router.get("/{customer_id}/credit-risk")
def customer_credit_risk(
    customer_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return calculate_customer_credit_score(
        db=db,
        tenant_id=current_user.tenant_id,
        customer_id=customer_id
    )

from src.domains.customer_finance.services.credit_dashboard_service import (
    get_credit_risk_dashboard
)


@router.get("/analytics/credit-risk-dashboard")
def credit_risk_dashboard(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_credit_risk_dashboard(
        db=db,
        tenant_id=current_user.tenant_id
    )


from src.domains.customer_finance.services.credit_risk_engine_service import (
    recalculate_customer_credit_risk
)


@router.post("/{customer_id}/credit-risk/recalculate")
def recalculate_credit_risk(
    customer_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return recalculate_customer_credit_risk(
        db=db,
        tenant_id=current_user.tenant_id,
        customer_id=customer_id
    )


from src.domains.customer_finance.services.credit_behavior_service import (
    analyze_credit_behavior
)


@router.get("/{customer_id}/credit-behavior")
def credit_behavior(
    customer_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return analyze_credit_behavior(
        db=db,
        tenant_id=current_user.tenant_id,
        customer_id=customer_id
    )


from src.domains.customer_finance.services.credit_decision_service import (
    make_credit_decision
)


@router.post("/{customer_id}/credit-decision")
def credit_decision(
    customer_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return make_credit_decision(
        db=db,
        tenant_id=current_user.tenant_id,
        customer_id=customer_id
    )


from src.domains.customer_finance.services.credit_action_service import (
    apply_credit_decision
)


@router.post("/{customer_id}/credit-decision/apply")
def apply_credit_action(
    customer_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return apply_credit_decision(
        db=db,
        tenant_id=current_user.tenant_id,
        customer_id=customer_id
    )

from src.domains.customer_finance.services.credit_history_service import (
    get_customer_credit_history
)


@router.get("/{customer_id}/credit-history")
def customer_credit_history(
    customer_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_customer_credit_history(
        db=db,
        tenant_id=current_user.tenant_id,
        customer_id=customer_id
    )

from src.domains.customer_finance.services.high_risk_monitor_service import (
    get_high_risk_customers
)


@router.get("/analytics/high-risk-customers")
def high_risk_customers(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_high_risk_customers(
        db=db,
        tenant_id=current_user.tenant_id
    )


from src.domains.customer_finance.services.credit_alert_service import (
    create_credit_alert
)


@router.post("/{customer_id}/credit-alert")
def create_alert(
    customer_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return create_credit_alert(
        db=db,
        tenant_id=current_user.tenant_id,
        customer_id=customer_id,
        alert_type="HIGH_RISK",
        severity="WARNING",
        message="Credit review required"
    )

from src.domains.customer_finance.services.credit_alert_list_service import get_credit_alerts


@router.get("/alerts")
def credit_alerts(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_credit_alerts(
        db=db,
        tenant_id=current_user.tenant_id
    )

from src.domains.customer_finance.services.credit_alert_update_service import resolve_credit_alert


@router.post("/alerts/{alert_id}/resolve")
def resolve_alert(
    alert_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return resolve_credit_alert(
        db=db,
        tenant_id=current_user.tenant_id,
        alert_id=alert_id
    )


from src.domains.customer_finance.services.credit_action_history_service import (
    get_credit_actions
)


@router.get("/actions")
def credit_action_history(
    customer_id: str | None = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_credit_actions(
        db=db,
        tenant_id=current_user.tenant_id,
        customer_id=customer_id
    )
